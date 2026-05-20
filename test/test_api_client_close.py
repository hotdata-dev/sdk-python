import unittest

from hotdata import ApiClient


class TestApiClientClose(unittest.TestCase):
    def test_close_does_not_raise(self) -> None:
        client = ApiClient()
        client.close()

    def test_context_manager_calls_close(self) -> None:
        client = ApiClient()
        called = False
        original_close = client.rest_client.close

        def tracked_close() -> None:
            nonlocal called
            called = True
            original_close()

        client.rest_client.close = tracked_close
        with client:
            pass
        self.assertTrue(called)


if __name__ == "__main__":
    unittest.main()
