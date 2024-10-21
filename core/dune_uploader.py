import dotenv
import os
from dune_client.client import DuneClient


def upload_data(csv_file_path, table_name, description="Measuring the Concentration of Power in the Collective"):
    # change the current working directory where .env file lives
    os.chdir("./")
    # load .env file
    dotenv.load_dotenv(".env")
    # setup Dune Python client
    dune = DuneClient.from_env()

    with open(csv_file_path) as open_file:
        data = open_file.read()

        table = dune.upload_csv(
            data=str(data),
            description=description,
            table_name=table_name,
            is_private=False
        )


if __name__ == "__main__":
    upload_data(
        '/Users/bilalbai/Documents/Git/op-vica/results/logit_effects.csv', 'logit_effects')
