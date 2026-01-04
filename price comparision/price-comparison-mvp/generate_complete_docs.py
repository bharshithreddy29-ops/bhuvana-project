import os

def generate_complete_docs():
    output_file = 'COMPLETE_PROJECT_DOCUMENTATION.md'
    
    # Files to combine in specific order
    files_to_combine = [
        ('PROJECT_SUMMARY.md', 'Project Overview'),
        ('README.md', 'Basic Setup & Usage'),
        ('README_ML.md', 'AI/ML Platform Documentation'),
        ('ENHANCED_FEATURES.md', 'Detailed Features List'),
        ('LIVE_SEARCH_SETUP.md', 'Live Search Configuration'),
        ('DEPLOYMENT.md', 'Deployment Guide'),
        ('ALL_DATASETS_DOCUMENTATION.txt', 'Appendix: Dataset Reference')
    ]
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        # Master Title
        outfile.write("# PriceHunter - Complete Project Documentation\n")
        outfile.write(f"Generated on: {os.path.basename(os.getcwd())}\n\n")
        outfile.write("This document contains all technical details, setup instructions, feature guides, and dataset references for the Price Comparison AI/ML Platform.\n\n")
        outfile.write("---\n\n")
        
        # Table of Contents
        outfile.write("## Table of Contents\n\n")
        for filename, title in files_to_combine:
            if os.path.exists(filename):
                outfile.write(f"- [{title}](#{title.lower().replace(' ', '-').replace('/', '').replace(':', '')})\n")
        outfile.write("\n---\n\n")
        
        # Combine Files
        for filename, title in files_to_combine:
            if os.path.exists(filename):
                print(f"Processing {filename}...")
                outfile.write(f"\n\n# {title}\n")
                outfile.write(f"(Source: {filename})\n\n")
                outfile.write("---\n\n")
                
                try:
                    with open(filename, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        outfile.write(content)
                        outfile.write("\n\n---\n")
                except Exception as e:
                    outfile.write(f"\nError reading file: {e}\n")
            else:
                print(f"Warning: {filename} not found")

    print(f"\n✓ Complete documentation generated: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    generate_complete_docs()
