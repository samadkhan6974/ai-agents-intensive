import re
import wikipedia
from difflib import get_close_matches

def _normalize_typo(q):
    # collapse repeated letters: "maachine" -> "machine"
    return re.sub(r'(.)\1{1,}', r'\1', q)

def search_wikipedia(query):
    """Robust Wikipedia search with suggestions and simple typo handling."""
    try:
        wikipedia.set_lang("en")
        query = query.strip()

        # 1) direct search
        results = wikipedia.search(query)
        if results:
            # pick best match
            title = results[0]
            summary = wikipedia.summary(title, sentences=3)
            return f"📘 {title}:\n{summary}"

        # 2) use library suggestion (e.g. "machine learning")
        suggestion = wikipedia.suggest(query)
        if suggestion:
            # ask user implicitly — but here we auto-use suggestion
            # you can also ask user: "Did you mean ... ?"
            results = wikipedia.search(suggestion)
            if results:
                title = results[0]
                summary = wikipedia.summary(title, sentences=3)
                return f"🔁 No exact match, showing results for suggested term: '{suggestion}'\n\n📘 {title}:\n{summary}"

        # 3) try simple normalization (fix repeated letters, common typos)
        normalized = _normalize_typo(query)
        if normalized != query:
            results = wikipedia.search(normalized)
            if results:
                title = results[0]
                summary = wikipedia.summary(title, sentences=3)
                return f"🔁 Tried normalized term '{normalized}':\n\n📘 {title}:\n{summary}"

        # 4) last attempt: wide search using parts of the query
        parts = [p for p in re.split(r'[\s\-_,]+', query) if len(p) > 2]
        combined_results = []
        for p in parts:
            combined_results.extend(wikipedia.search(p))
        combined_results = list(dict.fromkeys(combined_results))  # unique preserve order

        if combined_results:
            # show top 5 and let user pick (or auto-return first)
            top = combined_results[:5]
            return "No exact match found. Here are possible related pages:\n- " + "\n- ".join(top) + \
                   "\n\nTry one of these keywords or retype more clearly."

        return "No matching topics found. Try another keyword or check spelling."

    except wikipedia.exceptions.DisambiguationError as e:
        # present a few options
        options = e.options[:7]
        return f"Too many possible results — maybe try one of these:\n- " + "\n- ".join(options)
    except wikipedia.exceptions.PageError:
        return "Couldn't find a page for that topic. Try rephrasing!"
    except Exception as e:
        return f"An error occurred: {str(e)}"
