"""
Custom sorting and searching algorithms with performance benchmarking.
Implements from scratch and compares with built-in alternatives.
"""
import time
from typing import List, Callable, Any, Optional, Tuple


# ============================================================================
# SORTING ALGORITHMS
# ============================================================================

def merge_sort(data: List[Any], key: Callable = None) -> List[Any]:
    """
    Merge sort implementation: O(n log n) time complexity.
    Stable sorting algorithm, efficient for large datasets.
    
    Args:
        data: List to sort
        key: Function to extract comparison key from each element
        
    Returns:
        Sorted list
    """
    if len(data) <= 1:
        return data

    # Base case: single element is sorted
    if key is None:
        key = lambda x: x

    def merge(left: List, right: List) -> List:
        """Merge two sorted lists."""
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # Divide
    mid = len(data) // 2
    left = merge_sort(data[:mid], key)
    right = merge_sort(data[mid:], key)

    # Conquer
    return merge(left, right)


def quick_sort(data: List[Any], key: Callable = None) -> List[Any]:
    """
    Quick sort implementation: O(n log n) average, O(n²) worst case.
    Fast in practice for most datasets.
    
    Args:
        data: List to sort
        key: Function to extract comparison key
        
    Returns:
        Sorted list
    """
    if len(data) <= 1:
        return data

    if key is None:
        key = lambda x: x

    # Choose pivot (middle element)
    pivot = data[len(data) // 2]
    pivot_key = key(pivot)

    # Partition
    left = [x for x in data if key(x) < pivot_key]
    middle = [x for x in data if key(x) == pivot_key]
    right = [x for x in data if key(x) > pivot_key]

    # Recursively sort
    return quick_sort(left, key) + middle + quick_sort(right, key)


def bubble_sort(data: List[Any], key: Callable = None) -> List[Any]:
    """
    Bubble sort: O(n²) time complexity.
    Inefficient for large datasets, included for comparison.
    
    Args:
        data: List to sort
        key: Function to extract comparison key
        
    Returns:
        Sorted list
    """
    if key is None:
        key = lambda x: x

    result = data.copy()
    n = len(result)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if key(result[j]) > key(result[j + 1]):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result


class SortingBenchmark:
    """Benchmark different sorting algorithms."""

    @staticmethod
    def benchmark(data: List, algorithm_name: str,
                  key: Callable = None) -> Tuple[float, List]:
        """
        Benchmark a sorting algorithm.
        
        Args:
            data: Data to sort
            algorithm_name: "merge", "quick", "bubble", "builtin"
            key: Sorting key function
            
        Returns:
            Tuple of (execution_time_seconds, sorted_result)
        """
        if algorithm_name == "merge":
            algo = merge_sort
        elif algorithm_name == "quick":
            algo = quick_sort
        elif algorithm_name == "bubble":
            algo = bubble_sort
        elif algorithm_name == "builtin":
            algo = lambda d, k: sorted(d, key=k or (lambda x: x))
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        start = time.perf_counter()
        result = algo(data, key)
        end = time.perf_counter()

        return (end - start, result)

    @staticmethod
    def compare_algorithms(data: List, key: Callable = None) -> dict:
        """
        Compare all sorting algorithms on the same data.
        
        Returns:
            Dictionary with timing for each algorithm
        """
        results = {}
        for algo_name in ["merge", "quick", "bubble", "builtin"]:
            elapsed, _ = SortingBenchmark.benchmark(
                data.copy(), algo_name, key
            )
            results[algo_name] = elapsed

        return results


# ============================================================================
# SEARCHING ALGORITHMS
# ============================================================================

def linear_search(data: List, target: Any, key: Callable = None) -> Optional[int]:
    """
    Linear search: O(n) time complexity.
    Works on unsorted data.
    
    Args:
        data: List to search
        target: Value to find
        key: Function to extract comparison key
        
    Returns:
        Index of target or None if not found
    """
    if key is None:
        key = lambda x: x

    target_key = key(target) if callable(target) else target

    for i, item in enumerate(data):
        if key(item) == target_key:
            return i

    return None


def binary_search(data: List, target: Any, key: Callable = None) -> Optional[int]:
    """
    Binary search: O(log n) time complexity.
    Requires sorted data!
    
    Args:
        data: Sorted list to search
        target: Value to find
        key: Function to extract comparison key
        
    Returns:
        Index of target or None if not found
    """
    if key is None:
        key = lambda x: x

    target_key = key(target) if callable(target) else target
    left, right = 0, len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_key = key(data[mid])

        if mid_key == target_key:
            return mid
        elif mid_key < target_key:
            left = mid + 1
        else:
            right = mid - 1

    return None


def binary_search_recursive(data: List, target: Any,
                            key: Callable = None,
                            left: int = 0,
                            right: Optional[int] = None) -> Optional[int]:
    """
    Binary search (recursive implementation).
    
    Args:
        data: Sorted list
        target: Value to find
        key: Comparison key function
        left: Left boundary
        right: Right boundary
        
    Returns:
        Index or None
    """
    if key is None:
        key = lambda x: x

    if right is None:
        right = len(data) - 1

    if left > right:
        return None

    target_key = key(target) if callable(target) else target
    mid = (left + right) // 2
    mid_key = key(data[mid])

    if mid_key == target_key:
        return mid
    elif mid_key < target_key:
        return binary_search_recursive(data, target, key, mid + 1, right)
    else:
        return binary_search_recursive(data, target, key, left, mid - 1)


class SearchingBenchmark:
    """Benchmark searching algorithms."""

    @staticmethod
    def benchmark(data: List, target: Any, algorithm_name: str,
                  key: Callable = None) -> Tuple[float, Optional[int]]:
        """
        Benchmark a search algorithm.
        
        Args:
            data: Data to search
            target: Value to find
            algorithm_name: "linear", "binary", "builtin"
            key: Searching key function
            
        Returns:
            Tuple of (execution_time, result_index)
        """
        if algorithm_name == "linear":
            algo = linear_search
        elif algorithm_name == "binary":
            algo = binary_search
        elif algorithm_name == "binary_recursive":
            algo = binary_search_recursive
        elif algorithm_name == "builtin":
            def builtin_search(d, t, k):
                try:
                    return d.index(t)
                except ValueError:
                    return None
            algo = builtin_search
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        start = time.perf_counter()
        result = algo(data, target, key) if algorithm_name != "builtin" else algo(data, target, None)
        end = time.perf_counter()

        return (end - start, result)

    @staticmethod
    def compare_algorithms(data: List, target: Any,
                          key: Callable = None) -> dict:
        """
        Compare search algorithms on the same data.
        Note: binary searches require sorted data.
        
        Returns:
            Dictionary with timing for each algorithm
        """
        results = {}

        # Linear search on unsorted data
        elapsed, _ = SearchingBenchmark.benchmark(
            data, target, "linear", key
        )
        results["linear"] = elapsed

        # Sort data first for binary search
        sorted_data = sorted(data, key=key or (lambda x: x))

        # Binary searches on sorted data
        for algo_name in ["binary", "binary_recursive", "builtin"]:
            elapsed, _ = SearchingBenchmark.benchmark(
                sorted_data, target, algo_name, key
            )
            results[algo_name] = elapsed

        return results


# ============================================================================
# COMPLEXITY ANALYSIS
# ============================================================================

class ComplexityAnalysis:
    """Big-O complexity documentation and analysis."""

    ALGORITHMS = {
        "bubble_sort": {
            "best": "O(n)",
            "average": "O(n²)",
            "worst": "O(n²)",
            "space": "O(1)",
            "stable": True,
            "description": "Simple but inefficient. Good for learning.",
        },
        "merge_sort": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n log n)",
            "space": "O(n)",
            "stable": True,
            "description": "Divide-and-conquer. Consistent performance.",
        },
        "quick_sort": {
            "best": "O(n log n)",
            "average": "O(n log n)",
            "worst": "O(n²)",
            "space": "O(log n)",
            "stable": False,
            "description": "Fast in practice. Used by Python's sort().",
        },
        "linear_search": {
            "best": "O(1)",
            "average": "O(n)",
            "worst": "O(n)",
            "space": "O(1)",
            "description": "Works on unsorted data.",
        },
        "binary_search": {
            "best": "O(1)",
            "average": "O(log n)",
            "worst": "O(log n)",
            "space": "O(1) iterative, O(log n) recursive",
            "description": "Requires sorted data. Very efficient.",
        },
    }

    @staticmethod
    def get_analysis(algorithm_name: str) -> dict:
        """Get complexity analysis for an algorithm."""
        return ComplexityAnalysis.ALGORITHMS.get(
            algorithm_name,
            {"error": "Algorithm not found"}
        )

    @staticmethod
    def print_report() -> str:
        """Generate a summary report of all algorithms."""
        report = "\n" + "="*70 + "\n"
        report += "ALGORITHM COMPLEXITY ANALYSIS\n"
        report += "="*70 + "\n\n"

        for algo_name, info in ComplexityAnalysis.ALGORITHMS.items():
            report += f"{algo_name.upper()}\n"
            report += f"  Best:     {info.get('best', 'N/A')}\n"
            report += f"  Average:  {info.get('average', 'N/A')}\n"
            report += f"  Worst:    {info.get('worst', 'N/A')}\n"
            report += f"  Space:    {info.get('space', 'N/A')}\n"
            if "stable" in info:
                report += f"  Stable:   {info['stable']}\n"
            report += f"  Notes:    {info.get('description', 'N/A')}\n"
            report += "\n"

        return report
