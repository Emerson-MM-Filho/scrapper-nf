import argparse
from scrapper import Scrapper

parser = argparse.ArgumentParser(
    prog="scrapper.py",
    epilog="See repo: https://github.com/Emerson-MM-Filho/scrapper-nf-sc",
    description="Scrapper Nota Fiscal Eletrônica Florianópolis.",
    fromfile_prefix_chars="@"
)

parser.add_argument(
    "-cmc",
    "--codigomunicipal",
    type=int,
    help="Código municipal",
    dest="cmc",
    required=True,
)
parser.add_argument(
    "-e",
    "--email",
    type=str,
    help="Email",
    dest="email",
    required=True,
)
parser.add_argument(
    "-p",
    "--password",
    type=str,
    help="Senha",
    dest="password",
    required=True,
)
parser.add_argument(
    "-cl",
    "--clonelast",
    help="Should clone the last transmited fiscal note",
    dest="should_clone_last",
    action="store_true",
    default=False,
    required=False,
)
parser.add_argument(
    "-d",
    "--download",
    help="Should Download the last trasmited fiscal note",
    dest="should_download_last",
    action="store_true",
    default=False,
    required=False,
)

args = parser.parse_args()

if __name__ == "__main__":
    scrapper = Scrapper(args.cmc, args.email, args.password)
    scrapper.login()

    if args.should_clone_last:
        scrapper.clone_last_consult_result()

    if args.should_download_last:
        scrapper.download_last_consult_result()

    while(True):
        pass