import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from src.config import REQUEST_TIMEOUT, USER_AGENT

class WebContent:
    def __init__(self, url: str, html: str, soup: BeautifulSoup):
        self.url = url
        self.html = html
        self.soup = soup
        self.title = self._extract_title()
        self.meta_description = self._extract_meta_description()
        self.h1 = self._extract_h1()
        self.headings = self._extract_headings()
        self.body_text = self._extract_body_text()
        self.images = self._extract_images()
        self.links = self._extract_links()
        self.word_count = len(self.body_text.split())
    
    def _extract_title(self) -> Optional[str]:
        title_tag = self.soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
    
    def _extract_meta_description(self) -> Optional[str]:
        meta = self.soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '').strip() if meta else None
    
    def _extract_h1(self) -> Optional[str]:
        h1_tag = self.soup.find('h1')
        return h1_tag.get_text().strip() if h1_tag else None
    
    def _extract_headings(self) -> Dict[str, List[str]]:
        headings = {}
        for i in range(1, 7):
            tag_name = f'h{i}'
            tags = self.soup.find_all(tag_name)
            headings[tag_name] = [tag.get_text().strip() for tag in tags]
        return headings
    
    def _extract_body_text(self) -> str:
        for tag in self.soup(['script', 'style', 'nav', 'header', 'footer']):
            tag.decompose()
        
        text = self.soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())
    
    def _extract_images(self) -> List[Dict]:
        images = []
        for img in self.soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt', '').strip())
            })
        return images
    
    def _extract_links(self) -> List[Dict]:
        links = []
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            is_internal = not href.startswith(('http://', 'https://')) or self.url in href
            links.append({
                'href': href,
                'text': link.get_text().strip(),
                'is_internal': is_internal,
                'is_external': not is_internal,
                'nofollow': 'nofollow' in link.get('rel', [])
            })
        return links

def fetch_content(url: str) -> WebContent:
    headers = {'User-Agent': USER_AGENT}
    
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        return WebContent(url, response.text, soup)
    
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout: URL took longer than {REQUEST_TIMEOUT}s to respond")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection failed: Unable to reach the URL")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error {response.status_code}: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")
