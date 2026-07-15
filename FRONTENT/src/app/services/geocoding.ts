export async function reverseGeocode(
    lat:number,
    lon:number
){
    // -------------------------
    // 1) OpenStreetMap
    // -------------------------

    try{
        const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lon}`,
            {
                headers: {
                    "Accept-Language": "en"
                }
            }
        );

        if(res.ok) {
            const data = await res.json();

            return{

            city:    
                data.address.city ||
                data.address.town ||
                data.address.village ||
                "",

            state:
                data.address.state ||"",
                
            
            country: 
                data.address.country || "",
            
            source: "Nominatim"

            };
        }
    }

    catch (err) {
        console.log("Nominatim Failed");
        
    }
    // -------------------------
    // 2) BigDataCloud
    // -------------------------

    try{
        const res = await fetch(
            `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`
        
        );

        if (res.ok) {

            const data = await res.json();

            return {

                city:
                    data.city ||
                    data.locality ||
                    "",

                state:
                    data.principalSubdivision ||
                    "",

                country:
                    data.countryName ||
                    "",

                source: "BigDataCloud"

            };

        }

    }

    catch {

        console.log("BigDataCloud failed");

    }

    // -------------------------
    // 3) GPS only
    // -------------------------

    return {

        city: "",
        state: "",
        country: "",
        source: "GPS"

    };

}