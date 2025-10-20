#!/usr/bin/env python3
"""
Simple Manufacturing Documents Uploader using RAGSearchTool
"""

import os
import sys
import glob
import time
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prism_core.core.tools.rag_search_tool import RAGSearchTool
from prism_core.core.tools.schemas import ToolRequest

def main():
    # Configuration
    weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    class_prefix = os.getenv("CLASS_PREFIX", "MANUFACTURE")  # Use MANUFACTURE prefix for separate class
    max_documents = int(os.getenv("MAX_DOCUMENTS", "100"))
    
    print(f"Starting Manufacturing Documents Upload to ManufactureCompliance")
    print(f"Weaviate URL: {weaviate_url}")
    print(f"Class: ManufactureCompliance (using {class_prefix} prefix)")
    print(f"Max Documents: {max_documents}")
    
    # Initialize RAGSearchTool with MANUFACTURE prefix
    rag_tool = RAGSearchTool(
        weaviate_url=weaviate_url,
        encoder_model=os.getenv("VECTOR_ENCODER_MODEL", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"),
        vector_dim=int(os.getenv("VECTOR_DIM", "768")),
        class_prefix=class_prefix,
        tool_type="api"
    )
    
    # Find all markdown documents
    base_path = "/app/data/manufacture_docs/markdown"
    categories = ["equipment_manual", "quality_control", "process_spec", "work_instruction"]
    
    all_files = []
    for category in categories:
        pattern = os.path.join(base_path, category, "*.md")
        files = glob.glob(pattern)
        all_files.extend(files)
        print(f"Found {len(files)} files in {category}")
    
    # Limit documents if specified
    if max_documents > 0:
        all_files = all_files[:max_documents]
    
    print(f"\nProcessing {len(all_files)} documents...")
    
    # Process each document
    successful = 0
    failed = 0
    
    for i, file_path in enumerate(all_files, 1):
        try:
            filename = os.path.basename(file_path)
            print(f"[{i}/{len(all_files)}] Uploading: {filename}")
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from first line
            lines = content.split('\n')
            title = lines[0].replace('#', '').strip() if lines else filename
            
            # Determine category from path
            category = ""
            for cat in categories:
                if cat in file_path:
                    category = cat
                    break
            
            # Create document for upload
            document = {
                "title": title,
                "content": content,
                "metadata": {
                    "filename": filename,
                    "category": category,
                    "source": "semiconductor_manufacturing_docs",
                    "document_type": "manufacturing_compliance",
                    "language": "ko"  # Korean manufacturing documents
                }
            }
            
            # Upload document to compliance domain
            result = rag_tool.upload_documents([document], domain="compliance")
            
            if result and result.get('success', False):
                successful += 1
                print(f"  ✓ Successfully uploaded")
            else:
                failed += 1
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
            
            # Small delay to avoid overwhelming
            if i % 10 == 0:
                time.sleep(1)
                
        except Exception as e:
            failed += 1
            print(f"  ✗ Error: {str(e)}")
            continue
    
    print(f"\n{'='*50}")
    print(f"Upload Complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {successful + failed}")
    
    # Verify upload with a test search
    if successful > 0:
        print(f"\nVerifying upload with test search...")
        from prism_core.core.tools.schemas import ToolRequest
        import asyncio
        
        async def test_search():
            test_request = ToolRequest(
                tool_name="rag_search",
                parameters={
                    "query": "semiconductor equipment maintenance",
                    "top_k": 3,
                    "domain": "compliance"
                }
            )
            
            result = await rag_tool.execute(test_request)
            if result.success:
                data = result.to_dict().get('data', {})
                results = data.get('results', [])
                print(f"✓ Found {len(results)} results")
                for idx, res in enumerate(results[:3], 1):
                    print(f"  {idx}. {res.get('metadata', {}).get('title', 'No title')[:50]}...")
            else:
                print("✗ Search verification failed")
        
        asyncio.run(test_search())

if __name__ == "__main__":
    main()