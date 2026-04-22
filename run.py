import sys
from wikiPage import get_page, get_n_closest_page

def run(start_title, dest_title, max_hops, top_n):
    current_page = get_page(start_title)
    destination_page = get_page(dest_title)

    if current_page is None:
        print(f"error: could not find start page {start_title!r}", file=sys.stderr)
        return 1
    if destination_page is None:
        print(f"error: could not find destination page {dest_title!r}", file=sys.stderr)
        return 1

    visited = [current_page["title"]]
    print(current_page["title"])

    for _ in range(max_hops):
        if current_page["title"] == destination_page["title"]:
            print(f"\nreached {destination_page['title']!r} in {len(visited) - 1} hops")
            return 0

        n_most_similar = get_n_closest_page(current_page, destination_page, top_n)
        if not n_most_similar:
            print("no outgoing links found. stopping.", file=sys.stderr)
            return 1

        if destination_page["title"] in (p["title"] for p in n_most_similar):
            current_page = destination_page
        else:
            next_page = next((c for c in n_most_similar if c["title"] not in visited), None)
            if next_page is None:
                print("no unvisited candidates left", file=sys.stderr)
                return 1
            current_page = next_page

        visited.append(current_page["title"])
        print(current_page["title"])

    print(f"\nhop cap reached ({max_hops}) without reaching {dest_title!r}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    start = input("start page: ").strip()
    destination = input("destination page: ").strip()
    sys.exit(run(start, destination, max_hops=15, top_n=10))