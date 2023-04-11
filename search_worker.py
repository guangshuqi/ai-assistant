import asyncio
# Import the required summarization library
# ...

def search_worker(search_queue, bot):
    while True:
        search_task = search_queue.get()
        if search_task is None:
            break

        user_id, search_description, channel = search_task
        print(f"Searching for: {search_description}")
        
        # Perform search and store results in a suitable format
        # ...
        summarized_results = "Here are the search results. blah blah blah"

        # Summarize the search results using the summarization library (e.g., llm)
        # ...
        # summarized_results = ...

        # Send summarized search results to the channel
        asyncio.run_coroutine_threadsafe(channel.send(summarized_results), bot.loop)

        search_queue.task_done()
