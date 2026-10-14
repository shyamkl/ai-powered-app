from agent.deals.models import Base, Deal, DealSourceEvent
from agent.database.deal_store import engine


print()
print("===================================")
print("CREATING DEAL TABLES")
print("===================================")

print()
print("Database URL:")
print(engine.url.render_as_string(hide_password=True))

print()
print("Creating tables...")

Base.metadata.create_all(
    bind=engine,
    tables=[
        Deal.__table__,
        DealSourceEvent.__table__,
    ]
)

print()
print("Tables created successfully.")

print()
print("Tables found in metadata:")

for table_name in Base.metadata.tables.keys():
    print(
        " -",
        table_name
    )

print()
print("===================================")
print("DONE")
print("===================================")