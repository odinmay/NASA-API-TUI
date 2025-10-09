"""All API calls are handled by this class, the main application"""
import requests
from textual.widgets import Markdown


class API():
    def __init__(self, api_key):
        self.api_key = api_key

    # @staticmethod
    # def get_rover_photos(rover="curiosity", camera="all", sol=1, earth_date=None):
    #     """Get all photo data from the NASA Rover API"""
    #
    #     nasa_test_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={sol}&earth_date={earth_date}&api_key={api_key}"
    #
    #     response = requests.get(nasa_test_url)
    #
    #     print(response.status_code)
    #     pprint(response.json())

    def get_rover_manifest_json(self, rover_name="curiosity"):
        """Return API response with Rover Manifest"""
        manifest_url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}?api_key={self.api_key}"
        response = requests.get(manifest_url)
        return response.json()

    def format_manifest_to_markdown(self, manifest_json, rover_name: str) -> Markdown:
        """Create Manifest Table"""
        photo_manifest = manifest_json.get("photo_manifest")

        manifest_dict = {}
        manifest_dict["Name"] = photo_manifest.get("name")
        manifest_dict["Landing Date"] = photo_manifest.get("landing_date")
        manifest_dict["Launch Date"] = photo_manifest.get("launch_date")
        manifest_dict["Status"] = photo_manifest.get("status")
        manifest_dict["Max Sol"] = photo_manifest.get("max_sol")
        manifest_dict["Max Date"] = photo_manifest.get("max_date")
        manifest_dict["Total Photos"] = photo_manifest.get("total_photos")

        curiosity_description = """
        Curiosity is a car-sized Mars rover that is exploring Gale crater and Mount Sharp on Mars as 
        part of NASA's Mars Science Laboratory (MSL) mission. Launched in 2011 and landed the following year,
        the rover continues to operate more than a decade after its original two-year mission.

        Curiosity was launched from Cape Canaveral (CCAFS) on November 26, 2011, at 15:02:00 UTC and 
        landed on Aeolis Palus inside Gale crater on Mars on August 6, 2012, 05:17:57 UTC. 
        The Bradbury Landing site was less than 2.4 km (1.5 mi) from the center of the rover's touchdown
        target after a 560 million km (350 million mi) journey.

        Mission goals include an investigation of the Martian climate and geology, an assessment of
        whether the selected field site inside Gale has ever offered environmental conditions favorable
        for microbial life (including investigation of the role of water), and planetary habitability 
        studies in preparation for human exploration.
        """

        descriptions = {
            "curiosity": curiosity_description,
            "opportunity": "PLACEHOLDER",
            "spirit": "PLACEHOLDER"
        }

        markdown_str = f"""
        ## {manifest_dict["Name"]} Rover Manifest.
        # Launch Date: {manifest_dict["Launch Date"]}
        # Landing Date: {manifest_dict["Landing Date"]}
        # Status" {manifest_dict["Status"]}
        # Max Sol: {manifest_dict["Max Sol"]}
        # Max Date: {manifest_dict["Max Date"]}
        # Total Photos: {manifest_dict["Total Photos"]}

        {descriptions[rover_name]}

        """
        manifest_markdown = Markdown(markdown_str)

        return manifest_markdown

    def get_rover_markdown(self, rover_name: str):
        rover_json = self.get_rover_manifest_json(rover_name)

        manifest_markdown = self.format_manifest_to_markdown(rover_json)

        return manifest_markdown