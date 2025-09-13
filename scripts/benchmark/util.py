"""Utility functions for the benchmark scripts."""

# Changes made for metrics implementation (Issue #129):
#
# WHAT CHANGED:
# 1. Added proper HTTP headers (Content-Type, Accept, User-Agent) for consistent request testing
# 2. Added error handling for non-JSON responses (like /readme HTML redirects)
# 3. Enhanced response parsing to handle different content types


import os
import time

import httpx
from dotenv import load_dotenv

load_dotenv()


def make_request(
    host: str = "http://localhost:5000",
    route: str = "authenticate",
    profile: bool = True,
    timeout: float = 10.0,
) -> tuple[dict, float]:
    """Make a request to the authentication endpoint and return the response and elapsed time.

    Args:
        host: The host to make the request to
        route: The route to make the request to
        profile: Whether to fetch the profile information or not
        timeout: The timeout for the request

    Returns:
        Tuple of response JSON and elapsed time in seconds
    """
    with httpx.Client(follow_redirects=True, timeout=httpx.Timeout(timeout)) as client:
        if route == "authenticate":
            data = {
                "username": os.getenv("TEST_PRN"),
                "password": os.getenv("TEST_PASSWORD"),
                "profile": profile,
            }
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "Benchmark-Test/1.0",
            }
            start_time = time.time()
            response = client.post(
                f"{host}/{route}",
                json=data,
                headers=headers,
                follow_redirects=True,
            )
        else:
            headers = {"Accept": "application/json", "User-Agent": "Benchmark-Test/1.0"}
            start_time = time.time()
            response = client.get(
                f"{host}/{route}",
                headers=headers,
                follow_redirects=True,
            )
    elapsed_time = time.time() - start_time

    # Handle different response types
    try:
        return response.json(), elapsed_time
    except ValueError:
        # For non-JSON responses (like HTML redirects), return human-readable status info
        status_text = {
            200: "OK",
            308: "Permanent Redirect", 
            404: "Not Found",
            500: "Internal Server Error"
        }.get(response.status_code, f"HTTP {response.status_code}")
        
        content_type = response.headers.get("content-type", "unknown").split(";")[0]
        content_size = len(response.content)
        
        return {
            "status": f"{response.status_code} {status_text}",
            "content_type": content_type,
            "content_size_bytes": content_size,
            "content_size_human": f"{content_size} bytes" if content_size < 1024 else f"{content_size/1024:.1f} KB",
            "response_time_ms": round(elapsed_time * 1000, 2),
            "success": 200 <= response.status_code < 300,
        }, elapsed_time
