import csv
import re
from Bio import Entrez
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def fetch_paper_info(paper_urls):
    Entrez.email = 'your_email@example.com'  # 自分のメールアドレスに変更

    paper_info = []
    for url in paper_urls:
        if 'pubmed.ncbi.nlm.nih.gov' in url:
            pmid = re.search(r'/(\d+)/?$', url).group(1)
            handle = Entrez.efetch(db='pubmed', id=pmid, retmode='xml')
            record = Entrez.read(handle)['PubmedArticle']
            handle.close()

            paper = {}
            paper['PubMedURL'] = url
            abstract = record[0]['MedlineCitation']['Article'].get('Abstract', {}).get('AbstractText', '')
            abstract_text = ' '.join([abstract_text for abstract_text in abstract])
            abstract_text = re.sub('<.*?>', '', abstract_text)
            paper['Abstract'] = abstract_text
            article_type = record[0]['MedlineCitation'].get('Article', {}).get('PublicationTypeList', [])
            article_type_list = [str(article) for article in article_type]
            paper['ArticleType'] = '; '.join(article_type_list)
            paper['Title'] = record[0]['MedlineCitation']['Article'].get('ArticleTitle', '')
            paper['PublicationDate'] = record[0]['MedlineCitation']['Article'].get('Journal', {}).get('JournalIssue', {}).get('PubDate', {}).get('Year', '')
            paper['Journal'] = record[0]['MedlineCitation']['Article'].get('Journal', {}).get('Title', '')
        else:
            paper = {}
            paper['PubMedURL'] = url
            paper['Abstract'] = ''
            paper['ArticleType'] = ''
            paper['Title'] = ''
            paper['PublicationDate'] = ''
            paper['Journal'] = ''

        paper_info.append(paper)

    return paper_info

# CSVファイルからURLのリストを読み込む
filename = 'Food_supplementation.csv'
urls = []
with open(filename, mode='r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        urls.append(row[0])

# PubMedおよび非PubMedのURLから情報を取得
papers = fetch_paper_info(urls)

# 新しいCSVファイルに情報を書き込む
output_filename = 'Food_supplementation_with_info.csv'
with open(output_filename, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['PubMedURL', 'Abstract', 'ArticleType', 'Title', 'PublicationDate', 'Journal'])
    writer.writeheader()
    writer.writerows(papers)

print(f"情報が追加されたCSVファイル {output_filename} が作成されました。")
