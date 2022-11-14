import os
import argparse

from freq_add import freq_add_summarizer

parser = argparse.ArgumentParser()
parser.add_argument(
    "--text",
    "-t",
    help="Text file to summarize",
    default="texts/genesisgv70.txt",
    type=str
)
parser.add_argument(
    "--summ",
    "-s",
    help="Specify which summarizer to use",
    default="freq",
    type=str,
    )

def main():
    args = parser.parse_args()
    file = open(args.text, 'r', encoding='utf-8')
    text = file.read()
    file.close()

    write_path = "summaries"
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    result = ""
    if args.summ == "freq":
        result = freq_add_summarizer(text)
    with open(f"{write_path}/{os.path.basename(args.text)}", 'w', encoding='utf-8') as f:
            f.write(result)

if __name__ == "__main__":
    main()