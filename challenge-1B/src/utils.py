import os
import time
from typing import Union
from pathlib import Path

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def format_duration(seconds: float) -> str:
    """
    Format duration in human readable format
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.0f}s"
    else:
        hours = int(seconds // 3600)
        remaining_minutes = int((seconds % 3600) // 60)
        return f"{hours}h {remaining_minutes}m"

def validate_pdf_file(file_path: Union[str, Path]) -> tuple[bool, str]:
    """
    Validate if a file is a valid PDF
    
    Args:
        file_path: Path to the file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, "File does not exist"
        
        # Check file extension
        if path.suffix.lower() != '.pdf':
            return False, "File is not a PDF"
        
        # Check if file is readable
        if not os.access(path, os.R_OK):
            return False, "File is not readable"
        
        # Check file size (basic validation)
        if path.stat().st_size == 0:
            return False, "File is empty"
        
        # Try to read first few bytes to check PDF header
        with open(path, 'rb') as f:
            header = f.read(8)
            if not header.startswith(b'%PDF-'):
                return False, "File does not appear to be a valid PDF"
        
        return True, ""
        
    except Exception as e:
        return False, f"Error validating file: {str(e)}"

def create_temp_directory(base_dir: str = "/tmp") -> Path:
    """
    Create a temporary directory for processing
    
    Args:
        base_dir: Base directory for temporary files
        
    Returns:
        Path to created directory
    """
    import tempfile
    
    temp_dir = Path(tempfile.mkdtemp(dir=base_dir, prefix="pdf_processor_"))
    return temp_dir

def cleanup_temp_files(temp_dir: Union[str, Path]) -> bool:
    """
    Clean up temporary files and directories
    
    Args:
        temp_dir: Directory to clean up
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import shutil
        path = Path(temp_dir)
        
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            return True
        return False
        
    except Exception:
        return False

def estimate_processing_time(file_size_mb: float, page_count: int) -> float:
    """
    Estimate processing time based on file size and page count
    
    Args:
        file_size_mb: File size in MB
        page_count: Number of pages
        
    Returns:
        Estimated processing time in seconds
    """
    # Base processing time per page (empirical estimate)
    base_time_per_page = 0.1  # seconds
    
    # Additional time based on file size
    size_factor = file_size_mb * 0.02  # seconds per MB
    
    # Page complexity factor
    page_factor = page_count * base_time_per_page
    
    # Total estimated time with some buffer
    estimated_time = (page_factor + size_factor) * 1.2
    
    return max(0.5, estimated_time)  # Minimum 0.5 seconds

def get_system_resources() -> dict:
    """
    Get current system resource usage
    
    Returns:
        Dictionary with resource information
    """
    import psutil
    
    try:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        
        # Get disk usage for /tmp
        disk = psutil.disk_usage('/tmp')
        
        return {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": memory.available / (1024**3),
            "disk_free_gb": disk.free / (1024**3),
            "cpu_count": psutil.cpu_count()
        }
        
    except ImportError:
        # psutil not available, return basic info
        return {
            "cpu_percent": 0,
            "memory_percent": 0,
            "memory_available_gb": 16,  # Assume 16GB as per challenge requirements
            "disk_free_gb": 50,
            "cpu_count": 8  # As per challenge requirements
        }

def log_processing_metrics(filename: str, processing_time: float, page_count: int, 
                          file_size_mb: float, success: bool) -> None:
    """
    Log processing metrics for performance analysis
    
    Args:
        filename: Name of processed file
        processing_time: Time taken to process
        page_count: Number of pages processed
        file_size_mb: File size in MB
        success: Whether processing was successful
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    metrics = {
        "timestamp": timestamp,
        "filename": filename,
        "processing_time": processing_time,
        "page_count": page_count,
        "file_size_mb": file_size_mb,
        "success": success,
        "pages_per_second": page_count / processing_time if processing_time > 0 else 0,
        "mb_per_second": file_size_mb / processing_time if processing_time > 0 else 0
    }
    
    # In a production environment, this could be logged to a file or monitoring system
    print(f"METRICS: {metrics}")

def check_performance_constraints(processing_time: float, page_count: int, 
                                 memory_used_mb: float = 0) -> dict:
    """
    Check if processing meets the challenge performance constraints
    
    Args:
        processing_time: Time taken in seconds
        page_count: Number of pages processed
        memory_used_mb: Memory used in MB
        
    Returns:
        Dictionary with constraint validation results
    """
    results = {
        "time_constraint_met": True,
        "memory_constraint_met": True,
        "warnings": [],
        "performance_score": 100
    }
    
    # Check time constraint: ≤ 10 seconds for 50-page PDF
    expected_time = (page_count / 50) * 10  # Scale based on page count
    if processing_time > expected_time:
        results["time_constraint_met"] = False
        results["warnings"].append(f"Processing took {processing_time:.2f}s, expected ≤{expected_time:.2f}s")
        results["performance_score"] -= 30
    
    # Check memory constraint: Should stay well under 16GB
    memory_limit_mb = 16 * 1024  # 16GB in MB
    if memory_used_mb > memory_limit_mb * 0.8:  # 80% threshold
        results["memory_constraint_met"] = False
        results["warnings"].append(f"Memory usage {memory_used_mb:.1f}MB approaching limit")
        results["performance_score"] -= 20
    
    # Performance scoring
    if processing_time <= expected_time * 0.5:
        results["performance_score"] += 10  # Bonus for fast processing
    
    results["performance_score"] = max(0, min(100, results["performance_score"]))
    
    return results
