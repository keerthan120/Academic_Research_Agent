from agents import academic_coordinator


def main():

    topic = input("Enter research topic: ")

    papers, analysis = academic_coordinator(
        topic,
        "meta-llama/llama-3-8b-instruct"
    )

    print("\n========== PAPERS ==========\n")

    for i, paper in enumerate(papers, start=1):

        print(f"\nPaper {i}")

        print("Title:", paper["title"])

        print("Authors:", ", ".join(paper["authors"]))

        print("Published:", paper["published"])

        print("URL:", paper["url"])

        print("\nSummary:\n")

        print(paper["summary"])

        print("\n" + "=" * 60)

    print("\n========== AI ANALYSIS ==========\n")

    print(analysis)


if __name__ == "__main__":
    main()
