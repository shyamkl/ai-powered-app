class ProviderRanker:

    def __init__(self):
        self.history = {}

    def update(
        self,
        provider_name,
        venue_count,
        response_time,
        success=True
    ):

        if provider_name not in self.history:

            self.history[provider_name] = {
                "requests": 0,
                "success": 0,
                "venues": 0,
                "time": 0.0
            }

        h = self.history[provider_name]

        h["requests"] += 1

        if success:
            h["success"] += 1

        h["venues"] += venue_count

        h["time"] += response_time

    def score(self, provider_name):

        if provider_name not in self.history:
            return 0

        h = self.history[provider_name]

        success_rate = h["success"] / max(1, h["requests"])

        avg_time = h["time"] / max(1, h["requests"])

        avg_venues = h["venues"] / max(1, h["requests"])

        return (
            success_rate * 50
            + avg_venues * 0.2
            - avg_time * 5
        )

    def best_provider(self):

        if not self.history:
            return None

        return max(
            self.history,
            key=self.score
        )