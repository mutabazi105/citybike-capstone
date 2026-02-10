"""
Unit tests for CityBike algorithms module.
Tests sorting, searching, and algorithmic complexity analysis.
"""
import pytest
from citybike.algorithms import (
    merge_sort, quick_sort, bubble_sort,
    binary_search, binary_search_recursive, linear_search,
    SortingBenchmark, SearchingBenchmark, ComplexityAnalysis
)


class TestSortingAlgorithms:
    """Test cases for sorting algorithms."""

    @pytest.fixture
    def unsorted_lists(self):
        """Provide various unsorted lists for testing."""
        return {
            "basic": [3, 1, 4, 1, 5, 9, 2, 6],
            "already_sorted": [1, 2, 3, 4, 5],
            "reverse_sorted": [5, 4, 3, 2, 1],
            "single_element": [42],
            "empty": [],
            "duplicates": [5, 2, 5, 3, 2, 1, 5],
        }

    def test_merge_sort_basic(self, unsorted_lists):
        """Test merge sort with various inputs."""
        assert merge_sort(unsorted_lists["basic"]) == sorted(
            unsorted_lists["basic"])
        assert merge_sort(unsorted_lists["already_sorted"]) == [1, 2, 3, 4, 5]
        assert merge_sort(unsorted_lists["reverse_sorted"]) == [1, 2, 3, 4, 5]

    def test_merge_sort_edge_cases(self, unsorted_lists):
        """Test merge sort edge cases."""
        assert merge_sort(unsorted_lists["single_element"]) == [42]
        assert merge_sort(unsorted_lists["empty"]) == []
        assert merge_sort(unsorted_lists["duplicates"]) == sorted(
            unsorted_lists["duplicates"])

    def test_quick_sort_basic(self, unsorted_lists):
        """Test quick sort with various inputs."""
        assert quick_sort(unsorted_lists["basic"]) == sorted(
            unsorted_lists["basic"])
        assert quick_sort(unsorted_lists["already_sorted"]) == [1, 2, 3, 4, 5]
        assert quick_sort(unsorted_lists["duplicates"]) == sorted(
            unsorted_lists["duplicates"])

    def test_quick_sort_edge_cases(self, unsorted_lists):
        """Test quick sort edge cases."""
        assert quick_sort(unsorted_lists["single_element"]) == [42]
        assert quick_sort(unsorted_lists["empty"]) == []

    def test_bubble_sort_basic(self, unsorted_lists):
        """Test bubble sort with various inputs."""
        assert bubble_sort(unsorted_lists["basic"]) == sorted(
            unsorted_lists["basic"])
        assert bubble_sort(unsorted_lists["already_sorted"]) == [1, 2, 3, 4, 5]

    def test_bubble_sort_edge_cases(self, unsorted_lists):
        """Test bubble sort edge cases."""
        assert bubble_sort(unsorted_lists["single_element"]) == [42]
        assert bubble_sort(unsorted_lists["empty"]) == []

    def test_all_sorts_produce_identical_results(self, unsorted_lists):
        """Test that all sorting algorithms produce identical results."""
        test_list = unsorted_lists["duplicates"]

        merge_result = merge_sort(test_list.copy())
        quick_result = quick_sort(test_list.copy())
        bubble_result = bubble_sort(test_list.copy())

        assert merge_result == quick_result == bubble_result == sorted(
            test_list)


class TestSearchingAlgorithms:
    """Test cases for searching algorithms."""

    @pytest.fixture
    def sorted_list(self):
        """Provide a sorted list for searching."""
        return [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    def test_binary_search_found(self, sorted_list):
        """Test binary search finding elements."""
        assert binary_search(sorted_list, 1) == 0
        assert binary_search(sorted_list, 9) == 4
        assert binary_search(sorted_list, 19) == 9

    def test_binary_search_not_found(self, sorted_list):
        """Test binary search not finding elements."""
        assert binary_search(sorted_list, 2) == -1
        assert binary_search(sorted_list, 20) == -1
        assert binary_search(sorted_list, 0) == -1

    def test_binary_search_recursive_found(self, sorted_list):
        """Test recursive binary search finding elements."""
        assert binary_search_recursive(sorted_list, 1) == 0
        assert binary_search_recursive(sorted_list, 9) == 4
        assert binary_search_recursive(sorted_list, 19) == 9

    def test_binary_search_recursive_not_found(self, sorted_list):
        """Test recursive binary search not finding elements."""
        assert binary_search_recursive(sorted_list, 2) == -1
        assert binary_search_recursive(sorted_list, 20) == -1

    def test_linear_search_found(self, sorted_list):
        """Test linear search finding elements."""
        assert linear_search(sorted_list, 1) == 0
        assert linear_search(sorted_list, 9) == 4
        assert linear_search(sorted_list, 19) == 9

    def test_linear_search_not_found(self, sorted_list):
        """Test linear search not finding elements."""
        assert linear_search(sorted_list, 2) == -1
        assert linear_search(sorted_list, 20) == -1

    def test_linear_search_duplicates(self):
        """Test linear search with duplicate values."""
        test_list = [1, 3, 5, 5, 5, 7, 9]
        # Should find first occurrence
        assert linear_search(test_list, 5) == 2


class TestBenchmarkClasses:
    """Test cases for benchmarking classes."""

    def test_sorting_benchmark_initialization(self):
        """Test SortingBenchmark initialization."""
        benchmark = SortingBenchmark(sizes=[10, 50, 100])
        assert benchmark.sizes == [10, 50, 100]
        assert benchmark.iterations == 5

    def test_searching_benchmark_initialization(self):
        """Test SearchingBenchmark initialization."""
        benchmark = SearchingBenchmark(sizes=[10, 50, 100])
        assert benchmark.sizes == [10, 50, 100]

    def test_complexity_analysis_initialization(self):
        """Test ComplexityAnalysis initialization."""
        analysis = ComplexityAnalysis()
        assert analysis.algorithms is not None
        assert len(analysis.algorithms) > 0


class TestAlgorithmCorrectness:
    """Integration tests for algorithm correctness."""

    def test_sort_stability(self):
        """Test that sorting is stable (maintains relative order of equal elements)."""
        data = [(3, 'a'), (1, 'b'), (3, 'c'), (1, 'd')]
        # Extracting values only for comparison
        values = [x[0] for x in data]
        sorted_values = merge_sort(values.copy())
        assert sorted_values == [1, 1, 3, 3]

    def test_search_with_large_dataset(self):
        """Test searching with larger dataset."""
        large_list = list(range(0, 1000, 2))  # [0, 2, 4, ..., 998]

        # Test searching for existing values
        assert binary_search(large_list, 0) == 0
        assert binary_search(large_list, 500) >= 0

        # Test searching for non-existing values
        assert binary_search(large_list, 1) == -1
        assert binary_search(large_list, 999) == -1

    def test_sort_with_large_dataset(self):
        """Test sorting with larger dataset."""
        import random
        large_list = list(range(100))
        random.shuffle(large_list)

        sorted_list = merge_sort(large_list.copy())
        assert sorted_list == sorted(large_list)
        assert len(sorted_list) == 100
