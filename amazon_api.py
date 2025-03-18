import boto3
from botocore.exceptions import NoCredentialsError
import os
from dotenv import load_dotenv

load_dotenv()

class AmazonAPI:
    def __init__(self):
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.associate_tag = os.getenv("AWS_ASSOCIATE_TAG")
        self.client = boto3.client(
            "paapi5",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name="eu-west-3",  # Région AWS France
        )

    def get_product_info(self, asin):
        try:
            response = self.client.get_items(
                ItemIds=[asin],
                Resources=["Offers.Summaries.LowestPrice"],
                PartnerTag=self.associate_tag,
                PartnerType="Associates",
            )
            return response
        except NoCredentialsError:
            print("Erreur : Clés AWS non valides.")
            return None