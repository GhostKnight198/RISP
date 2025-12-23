#RISP v2
# ==============================================
# Research Index & Stats Program - Version 2
# Clean, documented, modular, readable
# ==============================================

from statistics import mean, median, stdev
import os

# ==============================================
# ======= Helper / Utility Functions ==========
# ==============================================

def print_divider(char="=", length=60):
    """
    Print a horizontal divider line.
    """
    print(char * length)


def get_int(prompt, min_val=None, max_val=None):
    """
    Prompt user for integer input.
    Validates that the input is integer and within optional min/max bounds.
    """
    while True:
        val = input(prompt).strip()
        if val.isdigit():
            val = int(val)
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"Value must be between {min_val} and {max_val}.")
                continue
            return val
        print("Invalid input. Enter a positive integer.")


def get_yes_no(prompt):
    """
    Prompt user for yes/no input.
    Returns 'y' or 'n'.
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans in ['y', 'n']:
            return ans
        print("Invalid input. Enter 'y' or 'n'.")


def print_paper_list(papers, title="Paper List"):
    """
    Nicely display papers with their citations in tabular format.
    """
    if not papers:
        print(f"\n{title}: No papers to display.\n")
        return
    print_divider()
    print(f"{title}".center(60))
    print_divider()
    print(f"{'S.No':<5} {'Paper Name':<35} {'Citations':>10}")
    print_divider('-')
    for i, (name, cit) in enumerate(papers.items(), start=1):
        print(f"{i:<5} {name:<35} {cit:>10}")
    print_divider()
    print()  # extra spacing


# ==============================================
# ======= Input / File Operations ============
# ==============================================

def get_paper_input():
    """
    Collect papers and their citation counts from the user.
    Auto-names papers if no name is given.
    Returns a dictionary: {paper_name: citations}.
    """
    papers = {}
    count = 1
    print("\nEnter paper names and citations. Type 'done' when finished.\n")
    while True:
        name = input(f"Paper name [{count}]: ").strip()
        if name.lower() == 'done':
            break
        if name == '':
            name = f"Paper {count}"
        citations = get_int(f"Citations for '{name}': ", min_val=0)
        papers[name] = citations
        count += 1
    return papers


def save_papers_to_txt(papers, filename):
    """
    Save paper dictionary to a TXT file in format: Paper Name|Citations.
    """
    try:
        with open(filename, 'w') as f:
            for name, cit in papers.items():
                f.write(f"{name}|{cit}\n")
        print(f"Papers saved to '{filename}' successfully.\n")
    except Exception as e:
        print(f"Error saving file: {e}\n")


def load_papers_from_txt(filename):
    """
    Load papers from TXT file in format: Paper Name|Citations.
    Returns a dictionary {name: citations}.
    """
    papers = {}
    if not os.path.exists(filename):
        print("File does not exist.\n")
        return papers
    try:
        with open(filename, 'r') as f:
            for line in f:
                if '|' in line:
                    name, cit = line.strip().split('|', 1)
                    if cit.isdigit():
                        papers[name] = int(cit)
        print(f"Papers loaded from '{filename}' successfully.\n")
    except Exception as e:
        print(f"Error loading file: {e}\n")
    return papers


# ==============================================
# ======= Core Statistics / Analysis ==========
# ==============================================

def h_index(papers):
    """
    Calculate h-index: maximum value h such that h papers have at least h citations.
    """
    citations = sorted(papers.values(), reverse=True)
    h = 0
    for i, c in enumerate(citations, start=1):
        if c >= i:
            h = i
    return h


def i10_index(papers):
    """
    Calculate i10-index: number of papers with at least 10 citations.
    """
    return sum(1 for c in papers.values() if c >= 10)


def count_above_thresholds(papers, thresholds):
    """
    Count papers with citations above each threshold in a list.
    Returns a dictionary {threshold: count}.
    """
    return {t: sum(1 for c in papers.values() if c >= t) for t in thresholds}


def get_sorted_papers(papers, mode="citations"):
    """
    Return a sorted dictionary by 'citations' descending or 'name' ascending.
    """
    if mode == "citations":
        return dict(sorted(papers.items(), key=lambda x: x[1], reverse=True))
    elif mode == "name":
        return dict(sorted(papers.items(), key=lambda x: x[0]))
    return papers


def generate_summary_report(papers):
    """
    Generate a detailed summary report including:
    - Total papers, total citations
    - h-index, i10-index
    - Average, median, min, max, range
    - Zero-citation papers
    - Outliers beyond ±2*std deviation
    - Sorted paper list
    Returns the report as a string.
    """
    if not papers:
        return "No papers available.\n"

    values = list(papers.values())
    total_papers = len(values)
    total_citations = sum(values)
    avg_citations = round(mean(values), 2)
    median_citations = median(values)
    max_cit = max(values)
    min_cit = min(values)
    h_idx = h_index(papers)
    i10_idx = i10_index(papers)
    range_cit = max_cit - min_cit
    zero_cit = [name for name, c in papers.items() if c == 0]

    # Detect outliers
    outliers_high, outliers_low = [], []
    if total_papers > 1:
        std_dev = stdev(values)
        mean_val = mean(values)
        for name, cit in papers.items():
            if cit > mean_val + 2 * std_dev:
                outliers_high.append((name, cit))
            elif cit < mean_val - 2 * std_dev:
                outliers_low.append((name, cit))

    # Build report
    report = []
    report.append("RESEARCH PAPER STATISTICS".center(60))
    report.append("=" * 60)
    report.append(f"Total Papers       : {total_papers}")
    report.append(f"Total Citations    : {total_citations}")
    report.append(f"h-index            : {h_idx}")
    report.append(f"i10-index          : {i10_idx}")
    report.append(f"Average Citations  : {avg_citations}")
    report.append(f"Median Citations   : {median_citations}")
    report.append(f"Max Citations      : {max_cit}")
    report.append(f"Min Citations      : {min_cit}")
    report.append(f"Range              : {range_cit}")
    report.append(f"Zero-Citation Papers: {', '.join(zero_cit) if zero_cit else 'None'}")
    report.append(f"High Outliers (>2σ): {', '.join([f'{n}({c})' for n, c in outliers_high]) if outliers_high else 'None'}")
    report.append(f"Low Outliers (<2σ) : {', '.join([f'{n}({c})' for n, c in outliers_low]) if outliers_low else 'None'}")
    report.append("\nAll Papers Descending by Citations:")
    sorted_papers = get_sorted_papers(papers)
    report.append(f"{'S.No':<5} {'Paper Name':<35} {'Citations':>10}")
    report.append("-" * 50)
    for i, (name, cit) in enumerate(sorted_papers.items(), start=1):
        report.append(f"{i:<5} {name:<35} {cit:>10}")
    return "\n".join(report)


# ==============================================
# ======= Edit / Manage Papers ================
# ==============================================

def edit_paper(papers):
    """
    Edit, rename, or delete a paper entry.
    User selects the action for a specific paper.
    """
    if not papers:
        print("No papers to edit.\n")
        return
    print_paper_list(papers, title="Current Papers")
    name = input("Enter the paper name to edit/delete: ").strip()
    if name not in papers:
        print("Paper not found.\n")
        return
    action = input("Enter 'edit', 'rename', or 'delete': ").strip().lower()
    match action:
        case 'edit':
            new_cit = get_int(f"Enter new citation count for '{name}': ", min_val=0)
            papers[name] = new_cit
            print("Updated successfully.\n")
        case 'rename':
            new_name = input("Enter new name: ").strip()
            if new_name:
                papers[new_name] = papers.pop(name)
                print("Renamed successfully.\n")
        case 'delete':
            del papers[name]
            print("Deleted successfully.\n")
        case _:
            print("Invalid action.\n")


# ==============================================
# ======= Index Menu ==========================
# ==============================================

def index_menu(papers):
    """
    Display h-index, i10-index, or both for the papers.
    """
    print_divider()
    print(f"Total Papers: {len(papers)} | Total Citations: {sum(papers.values())}\n")
    if not papers:
        print("No papers entered.\n")
        return
    print("Select Index to Calculate:")
    print("1: h-index")
    print("2: i10-index")
    print("3: Both")
    choice = get_int("Enter 1, 2, or 3: ", 1, 3)
    match choice:
        case 1:
            print(f"h-index: {h_index(papers)}\n")
        case 2:
            print(f"i10-index: {i10_index(papers)}\n")
        case 3:
            print(f"h-index: {h_index(papers)}")
            print(f"i10-index: {i10_index(papers)}\n")


# ==============================================
# ======= Statistics Menu =====================
# ==============================================

def statistics_menu(papers):
    """
    Main statistics and filters menu.
    Uses match-case for options.
    """
    while True:
        print_divider()
        print("STATISTICS & FILTERS MENU".center(60))
        print_divider()
        print(" 1: Max Citations         2: Min Citations          3: Max & Min")
        print(" 4: Average               5: Median                6: Zero-Citation Papers")
        print(" 7: Papers Above Thresholds (Custom)")
        print(" 8: Citation Range Filter")
        print(" 9: Top N Most Cited Papers")
        print("10: Full Summary Report")
        print("11: Export Citation List")
        print("12: Export Summary Report")
        print("13: Edit/Delete Papers")
        print("14: Load Citations From File")
        print("15: Save Citations To File")
        print("16: Detect Outliers")
        print("17: Exit\n")

        choice = get_int("Enter choice (1-17): ", 1, 17)

        match choice:
            case 1:
                print(f"\nMax Citations: {max(papers.values())}\n")
            case 2:
                print(f"\nMin Citations: {min(papers.values())}\n")
            case 3:
                print(f"\nMax: {max(papers.values())} | Min: {min(papers.values())}\n")
            case 4:
                print(f"\nAverage Citations: {round(mean(papers.values()), 2)}\n")
            case 5:
                print(f"\nMedian Citations: {median(papers.values())}\n")
            case 6:
                zero_cits = [name for name, c in papers.items() if c == 0]
                print(f"\nZero-Citation Papers: {', '.join(zero_cits) if zero_cits else 'None'}\n")
            case 7:
                thr_input = input("\nEnter thresholds separated by commas (e.g., 10,25,50): ")
                thresholds = [int(t.strip()) for t in thr_input.split(',') if t.strip().isdigit()]
                counts = count_above_thresholds(papers, thresholds)
                print("\nCounts above thresholds:")
                for t, c in counts.items():
                    print(f">= {t:>3}: {c}")
                print()
            case 8:
                low = get_int("\nEnter minimum citation: ", 0)
                high = get_int("Enter maximum citation: ", low)
                filtered = {name: c for name, c in papers.items() if low <= c <= high}
                print_paper_list(filtered, title=f"Papers with citations {low}-{high}")
            case 9:
                N = get_int("\nEnter N for Top N papers: ", 1)
                top_n = dict(list(get_sorted_papers(papers).items())[:N])
                print_paper_list(top_n, title=f"Top {N} Most Cited Papers")
            case 10:
                print(generate_summary_report(papers))
                print()
            case 11:
                if get_yes_no("\nDo you want to save the citation list to TXT? (y/n): ") == 'y':
                    filename = input("Enter filename (e.g., list.txt): ").strip()
                    save_papers_to_txt(papers, filename)
            case 12:
                if get_yes_no("\nDo you want to save the summary report to TXT? (y/n): ") == 'y':
                    filename = input("Enter filename (e.g., summary.txt): ").strip()
                    try:
                        with open(filename, 'w') as f:
                            f.write(generate_summary_report(papers))
                        print(f"Summary report saved to '{filename}' successfully.\n")
                    except Exception as e:
                        print(f"Error saving summary: {e}\n")
            case 13:
                edit_paper(papers)
            case 14:
                filename = input("\nEnter filename to load citations from (e.g., list.txt): ").strip()
                loaded = load_papers_from_txt(filename)
                papers.update(loaded)
            case 15:
                filename = input("\nEnter filename to save citations (e.g., list.txt): ").strip()
                save_papers_to_txt(papers, filename)
            case 16:
                report = generate_summary_report(papers)
                print("\nOutlier Information:")
                lines = report.split('\n')
                for line in lines:
                    if "Outliers" in line:
                        print(line)
                print()
            case 17:
                print("Exiting statistics menu...\n")
                break

        if choice != 17:
            cont = get_yes_no("Continue in statistics menu? (y/n): ")
            if cont == 'n':
                print("Exiting statistics menu...\n")
                break


# ==============================================
# ======= Main Function =======================
# ==============================================

def RI_v2():
    """
    Main entry point for the Research Index & Stats Program V2.
    Collects papers, displays index menu, and launches statistics menu.
    """
    print_divider()
    print("RESEARCH INDEX & STATS PROGRAM - VERSION 2".center(60))
    print_divider()

    papers = get_paper_input()
    if not papers:
        print("\nNo papers entered. Exiting program.\n")
        return

    index_menu(papers)
    statistics_menu(papers)


# ==============================================
# ======= Program Entry Point =================
# ==============================================

if __name__ == "__main__":
    RI_v2()
