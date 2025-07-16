from fetch_content import get_latest_articles
from summarize import summarize_text, extract_concepts
from personalize import filter_new_articles
from memory import update_memory
from concepts import add_to_learned, add_to_future_list

def main():
    print("👋 Ready to learn today?")
    input("Press Enter to begin...")

    articles = get_latest_articles()
    new_articles = filter_new_articles(articles)

    if not new_articles:
        print("🎉 You’re all caught up!")
        return

    article = new_articles[0]
    summary = summarize_text(article["content"])
    print(f"\n📘 Topic: {article['title']}\n")
    print(summary)

    # NEW: Extract key concepts
    concepts = extract_concepts(article["content"])
    print("\n💡 Key Concepts from this article:")
    for i, concept in enumerate(concepts):
        print(f"{i + 1}. {concept}")

    # Ask user to choose a topic
    choice = input("\nWhich topic would you like to learn more about? (Enter number or 'none'): ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(concepts):
        selected = concepts[int(choice) - 1]
        print(f"\n🔍 Great! Let's learn more about {selected}...")

        # Use GPT to explain the selected topic
        explanation = summarize_text(f"Explain the AI concept: {selected} in beginner-friendly terms.")
        print(f"\n🧠 {selected}:\n{explanation}")

        add_to_learned(selected)

        # Save others to future list
        for i, concept in enumerate(concepts):
            if i != int(choice) - 1:
                add_to_future_list(concept)

    else:
        print("\n📌 Got it! Saving all concepts for later.")
        for concept in concepts:
            add_to_future_list(concept)

    # Ask for feedback
    feedback = input("\nWas this helpful? (yes/no): ").strip().lower()
    update_memory(article["title"], feedback)

    print("✅ Feedback and concepts saved. See you next time!")

if __name__ == "__main__":
    main()
