# spiral_core/shared_knowledge_queue.py
from multiprocessing import Queue
import logging

logger = logging.getLogger(__name__)

class SharedKnowledgeQueue:
    """
    A singleton-like class to provide a single instance of a multiprocessing Queue
    for inter-module communication (e.g., Apollo -> Kairos feedback).
    """
    _instance = None
    _queue = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedKnowledgeQueue, cls).__new__(cls)
            cls._queue = Queue()
            logger.info("SharedKnowledgeQueue initialized.")
        return cls._instance

    def get_queue(self):
        """Returns the multiprocessing Queue instance."""
        return self._queue

    def get_size(self):
        """Returns the current size of the queue."""
        try:
            return self._queue.qsize()
        except NotImplementedError:
            # qsize() is not reliable on all OS (e.g., macOS for fork-based multiprocessing)
            logger.warning("qsize() not implemented on this OS or not reliable. Cannot get queue size.")
            return -1 # Indicate not available
        except Exception as e:
            logger.error(f"Error getting queue size: {e}")
            return -2

    def clear(self):
        """Clears all items from the queue."""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except Exception as e:
                logger.error(f"Error clearing queue item: {e}")
        logger.info("SharedKnowledgeQueue cleared.")

# Example Usage (for independent testing if needed, though primarily for import)
if __name__ == "__main__":
    q_instance1 = SharedKnowledgeQueue()
    queue1 = q_instance1.get_queue()

    queue1.put("Hello from test 1")
    print(f"Queue size: {q_instance1.get_size()}")

    q_instance2 = SharedKnowledgeQueue()
    queue2 = q_instance2.get_queue() # Should be the same queue instance

    print(f"Item from queue2: {queue2.get()}")
    print(f"Queue size after get: {q_instance1.get_size()}")

    q_instance1.clear()
    print(f"Queue size after clear: {q_instance1.get_size()}")
