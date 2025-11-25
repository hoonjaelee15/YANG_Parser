#!/usr/bin/env python3
"""
O-RAN 15.0.0 Specification Downloader

This script attempts to download O-RAN 15.0.0 specifications from
the O-RAN specifications portal.
"""

import requests
import os
import sys
from pathlib import Path
import re
import json

# Base URLs
SPEC_PORTAL = "https://specifications.o-ran.org"
ORAN_MAIN = "https://www.o-ran.org"

def create_download_directory():
    """Create directory for downloaded specifications"""
    download_dir = Path("oran_specs_15.0.0")
    download_dir.mkdir(exist_ok=True)
    return download_dir

def get_portal_content():
    """Fetch content from specifications portal"""
    try:
        response = requests.get(SPEC_PORTAL, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error accessing portal: {e}")
        return None

def find_download_links(content, version="15.0.0"):
    """Search for download links in portal content"""
    links = []
    
    # Look for various link patterns
    patterns = [
        rf'href=["\']([^"\']*{version}[^"\']*)["\']',
        rf'url["\']?\s*[:=]\s*["\']([^"\']*{version}[^"\']*)["\']',
        rf'download["\']?\s*[:=]\s*["\']([^"\']*{version}[^"\']*)["\']',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content, re.I)
        links.extend(matches)
    
    # Also look for API endpoints
    api_patterns = [
        r'api[^"\']*spec[^"\']*',
        r'api[^"\']*download[^"\']*',
        r'api[^"\']*version[^"\']*',
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, content, re.I)
        links.extend(matches)
    
    return list(set(links))

def try_direct_download_patterns(version="15.0.0"):
    """Try common download URL patterns"""
    base_patterns = [
        f"{SPEC_PORTAL}/download/{version}",
        f"{SPEC_PORTAL}/api/specifications/{version}",
        f"{SPEC_PORTAL}/specifications/{version}",
        f"{SPEC_PORTAL}/v{version}",
        f"{SPEC_PORTAL}/oran-{version}",
    ]
    
    results = []
    for url in base_patterns:
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            if response.status_code == 200:
                results.append((url, response.status_code))
                print(f"✓ Found accessible URL: {url}")
        except:
            pass
    
    return results

def download_file(url, output_path):
    """Download a file from URL"""
    try:
        print(f"Downloading: {url}")
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}%", end='', flush=True)
        
        print(f"\n✓ Downloaded: {output_path}")
        return True
    except Exception as e:
        print(f"\n✗ Error downloading {url}: {e}")
        return False

def main():
    print("O-RAN 15.0.0 Specification Downloader")
    print("=" * 50)
    
    # Create download directory
    download_dir = create_download_directory()
    print(f"Download directory: {download_dir.absolute()}")
    
    # Try direct download patterns first
    print("\n1. Trying direct download patterns...")
    direct_urls = try_direct_download_patterns("15.0.0")
    
    # Get portal content
    print("\n2. Accessing specifications portal...")
    content = get_portal_content()
    
    if content:
        print(f"   Portal accessible (content length: {len(content)} bytes)")
        print("   Note: Portal is a Blazor SPA - requires JavaScript/browser")
        
        # Search for download links
        print("\n3. Searching for download links...")
        links = find_download_links(content, "15.0.0")
        if links:
            print(f"   Found {len(links)} potential links")
            for i, link in enumerate(links[:10], 1):
                print(f"   {i}. {link}")
        else:
            print("   No direct download links found in portal content")
    else:
        print("   Could not access portal")
    
    # Summary
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  - Download directory: {download_dir.absolute()}")
    print(f"  - Portal URL: {SPEC_PORTAL}")
    print("\nIf automatic download is not possible, please:")
    print("1. Visit https://specifications.o-ran.org")
    print("2. Navigate to version 15.0.0")
    print("3. Download the specifications you need")
    print(f"4. Save them to: {download_dir.absolute()}")

if __name__ == "__main__":
    main()

