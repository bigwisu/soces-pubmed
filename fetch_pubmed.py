import os
import sys
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from Bio import Entrez
from urllib.error import HTTPError

# Load environment variables from .env file
load_dotenv()

# Get email from environment variable
EMAIL = os.getenv("EMAIL")

if not EMAIL:
    print("Error: EMAIL not found in .env file.")
    sys.exit(1)

Entrez.email = EMAIL
Entrez.tool = "SocesPubMedDataFetcher"

def fetch_pubmed_data_bulk(query: str, max_results: int = 2000, batch_size: int = 500):
    """
    Fetches a large number of article data from PubMed using the WebHistory feature.
    """
    print(f"Searching PubMed for: '{query}'...")
    try:
        # Step 1: ESearch with usehistory="y"
        # This tells NCBI to cache the IDs on their server
        search_handle = Entrez.esearch(
            db="pubmed", 
            term=query, 
            retmax=max_results, 
            usehistory="y"
        )
        search_results = Entrez.read(search_handle)
        search_handle.close()

        count = int(search_results["Count"])
        webenv = search_results["WebEnv"]
        query_key = search_results["QueryKey"]
        
        # We cap the total records we want to fetch at max_results
        total_to_fetch = min(count, max_results)
        print(f"Found {count} total matching records on PubMed.")
        print(f"Fetching top {total_to_fetch} records in batches of {batch_size}...")

        all_articles = []

        # Step 2: EFetch in batches
        for start in range(0, total_to_fetch, batch_size):
            end = min(total_to_fetch, start + batch_size)
            print(f"  -> Downloading records {start + 1} to {end}...")
            
            # Simple retry mechanism for HTTP errors (e.g. timeout or server rate limiting)
            attempt = 0
            while attempt < 3:
                try:
                    fetch_handle = Entrez.efetch(
                        db="pubmed",
                        rettype="medline",
                        retmode="xml",
                        retstart=start,
                        retmax=batch_size,
                        webenv=webenv,
                        query_key=query_key,
                    )
                    records = Entrez.read(fetch_handle)
                    fetch_handle.close()
                    
                    batch_articles = records.get("PubmedArticle", [])
                    all_articles.extend(batch_articles)
                    break # Success, break retry loop
                    
                except HTTPError as err:
                    if 500 <= err.code <= 599:
                        print(f"    Server error ({err.code}), retrying in 5 seconds...")
                        time.sleep(5)
                        attempt += 1
                    else:
                        raise err # Raise for 4xx errors
                        
            # Sleep briefly to respect NCBI API rate limits (3 requests per second)
            time.sleep(1)
            
        return all_articles

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_article_info(pubmed_articles):
    """
    Extracts relevant information (like title and abstract) from the raw XML records.
    """
    extracted_data = []
    for pubmed_article in pubmed_articles:
        try:
            article = pubmed_article['MedlineCitation']['Article']
            pmid = str(pubmed_article['MedlineCitation']['PMID'])
            
            title = article.get('ArticleTitle', 'No title')
            
            abstract_text = 'No abstract'
            if 'Abstract' in article and 'AbstractText' in article['Abstract']:
                abstract_text = " ".join(article['Abstract']['AbstractText'])
                
            extracted_data.append({
                "PMID": pmid,
                "Title": title,
                "Abstract": abstract_text
            })
        except KeyError as e:
            # Skip records that might be missing standard keys
            continue
            
    return extracted_data

if __name__ == "__main__":
    # Define query and how many total records you want to download
    query = '"machine learning"[Title/Abstract]'
    max_results = 2000 # Download 2000 records
    
    # Define output file path
    project_root = Path(__file__).parent
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)
    output_file = data_dir / "pubmed_results_bulk.json"
    
    # Fetch and extract data
    raw_articles = fetch_pubmed_data_bulk(query, max_results=max_results, batch_size=200)
    
    if raw_articles:
        processed_data = extract_article_info(raw_articles)
        
        # Save to file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=4, ensure_ascii=False)
            
        print(f"\nSuccessfully saved {len(processed_data)} records to {output_file}")
    else:
        print("\nNo data to save.")
