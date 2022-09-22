<script>
    import { fade } from "svelte/transition";
    import { onMount } from "svelte";
    // store URLs as variables for future reference
    const pastReadUrl =
        "https://openlibrary.org/people/bendextercooley/books/already-read.json";
    const currentlyReadingUrl =
        "https://openlibrary.org/people/bendextercooley/books/currently-reading.json";
    const coverUrl = "http://covers.openlibrary.org/b/olid/";
    const olBookUrl = "https://openlibrary.org/books/";
    // create some empty variables for storing data later
    // these need to be before onMount so they are global, and can be used in the template
    let formattedBooks = [];
    let formattedReading = [];
    let bookList = [];
    let currentList = [];
    let finalBooks, nowReading, booksLength;
    onMount(async () => {
        currentList = await fetch(currentlyReadingUrl).then((x) => x.json());
        bookList = await fetch(pastReadUrl).then((x) => x.json());
        // console.log("data is ready: ", currentList);
        nowReading = formatData(currentList, formattedReading);
        finalBooks = formatData(bookList, formattedBooks);
        booksLength = finalBooks.length;
        console.log(nowReading);
    });
    // function to pull out the data that I want
    function formatData(dataObject, arr) {
        const colors = ["#730A16", "#BB4F24", "#2F7894", "#D28F33"];
        let widths = [60, 70, 90];
        // NOTE: datestamp on OpenLibrary is wrong for now :(
        // sort by date
        //       const dataset = formattedBooks.sort(function(a,b){
        //   return b.read_timestamp - a.read_timestamp;
        // });
        function getRandomInt(max) {
            return Math.floor(Math.random() * max);
        }
        // pull out relevant data
        dataObject.reading_log_entries.forEach((d) => {
            let obj = {};
            if (d.logged_edition == null) {
                obj.ol_id = d.work.key.split("/")[2];
            } else {
                obj.ol_id = d.logged_edition.split("/")[2];
            }
            (obj.title = d.work.title),
            (obj.color = colors[getRandomInt(4)]),
            (obj.width = widths[getRandomInt(3)]),
            (obj.tilt = getRandomInt(4) * 1.3),
            (obj.read_date = d.logged_date),
            (obj.read_timestamp = new Date(d.logged_date.split(",")[0])),
            (obj.book_link = d.work.key),
            (obj.cover_url =
                coverUrl + d.work.cover_edition_key + "-M.jpg"),
            (obj.author = d.work.author_names[0]),
            (obj.author_link = d.work.author_keys[0]);
            arr.push(obj);
        });
        return arr;
    }
    // when user clicks book, display info on left side
    let bookOffShelf;
    function pullOffShelf(data) {
        bookOffShelf = data;
    }
    // switch from bookshelf/list view
    let shelfView = true;
    function toggleView() {
        shelfView = !shelfView;
    }
</script>

<svelte:head>
    <title>Bookshelf</title>
</svelte:head>

<div id="book-page">
    <div>
        <div class="row">
            <div class="col-1">
                <h2 style="padding-bottom: 20px">Currently reading</h2>
                <p>On my coffee table or bedside table. You can find all the books I remember reading on my bookshelf below, which pulls live data from the <a href="https://openlibrary.org/" target="_blank">OpenLibrary</a> API. Read about why I made this library <a href="/notepad/my-digital-bookshelf">here</a>.</p>
            </div>
            <div class="col-2" style="min-height: 400px; margin-left: 20px;">
                {#if nowReading != null}
                    {#each nowReading as book}
                        <div in:fade
                            style="display: inline-block; margin-left: 10px; margin-right: 10px"
                        >
                            <img 
                                style="margin-bottom: 10px"
                                src={book.cover_url}
                                alt={book.title}
                            />
                            <h4>{book.title}</h4>
                            <p style="line-height: 1; margin-top: -5px">
                                by {book.author}
                            </p>
                            <a
                                style="line-height: 1margin-top: -30px"
                                href="{olBookUrl}{book.ol_id}"
                                target="_blank">View on OpenLibrary</a
                            >
                        </div>
                    {/each}
                    {:else}
                    <div>
                        <p style="text-align: center">Getting latest books...</p>
                        <div class="loader" style="margin: 0 auto"></div>
                    </div>
                {/if}
            </div>
        </div>
    </div>

    <div in:fade class="row">
        <div class="col-1">
            <h2 style="margin-bottom: 20px">Off the shelf</h2>
            <p>Click on a book to pull it off the shelf for more details.</p>
            {#if bookOffShelf != null}
                <img
                    style="margin-bottom: -20px"
                    src={bookOffShelf.cover_url}
                    alt=""
                />
                <h2>{bookOffShelf.title}</h2>
                <h4>by {bookOffShelf.author}</h4>
                <a href="{olBookUrl}{bookOffShelf.ol_id}" target="_blank"
                    >View on OpenLibrary</a
                >
            {/if}
        </div>
        <div class="col-2">
            {#if finalBooks != null}
                {#if shelfView}
                    <button class="toggle-btn" on:click={toggleView}>Show as 📋 list</button>
                {:else}
                    <button class="toggle-btn" on:click={toggleView}>Show as 📚 bookshelf</button>
                {/if}
                
                <span style="float: right; font-size: 20px">Total books read: <strong>{booksLength}</strong></span>
            {/if}
            <div id="container" style="width: 100%">
                {#if finalBooks != null}
                    {#if shelfView == true}
                        {#each finalBooks as book}
                            <div
                                class="book"
                                on:click={() => pullOffShelf(book)}
                                in:fade="{{ duration: 2000 }}"
                                style="background-color: {book.color}; transform: rotate({book.tilt}deg); width: {book.width}px"
                            >
                                <div class="spine">
                                    <p class="inner rotate">{book.title}</p>
                                </div>
                            </div>
                            {/each}
                        {:else}
                            {#each finalBooks as book}
                                <div class="row book-row" style="max-width: 450px" 
                                on:click={() => pullOffShelf(book)}
                                in:fade="{{ duration: 2000 }}">
                                    <div class="col-1">
                                            <img 
                                        style="margin-bottom: 10px; width: 100px"
                                        src={book.cover_url}
                                        alt={book.title}
                                    />
                                    </div>
                                    <div class="col-2">
                                        <h4>{book.title}</h4>
                                        <p style="line-height: 1; margin-top: -5px">
                                            by {book.author}
                                        </p>
                                        <a
                                            style="line-height: 1margin-top: -30px"
                                            href="{olBookUrl}{book.ol_id}"
                                            target="_blank">View on OpenLibrary</a
                                        >
                                    </div>
                                </div>
                            {/each}

                        {/if}
                {:else}
                    <div>
                        <p style="margin-left: 20px" id="loading">Organizing books on the shelf...</p>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>

<style>
    h1 {
        color: black;
    }
    #book-page {
        padding: 15px;
    }
    .book-row {
        border-bottom: 1px solid gray;
        margin-bottom: 10px
    }
    .row {
        display: flex;
        margin: 0 auto;
        padding: 10px;
    }
    .col-1 {
        flex: 1;
        width: 300px;
    }
    .col-2 {
        flex: 2;
    }
    #container {
        display: flex;
        flex-wrap: wrap;
        border: solid 2px brown;
        padding: 5px;
        margin: 20px;
        min-height: 500px;
    }
    .book {
        height: 270px;
        width: 60px;
        position: relative;
        display: inline-block;
        margin: 3px;
    }
    .inner {
        position: absolute;
        top: 50%;
        left: 40%;
        margin: 10px;
        width: 240px;
        font-size: 20px;
        color: white;
        font-weight: 600;
        text-align: center;
    }
    .loader {
        border: 16px solid #f3f3f3;
        border-radius: 50%;
        border-top: 16px solid #3498db;
        width: 120px;
        height: 120px;
        -webkit-animation: spin 2s linear infinite; /* Safari */
        animation: spin 2s linear infinite;
    }
    /* Safari */
    @-webkit-keyframes spin {
        0% {
            -webkit-transform: rotate(0deg);
        }
        100% {
            -webkit-transform: rotate(360deg);
        }
    }
    @keyframes spin {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    .toggle-btn {
        float: left; margin-left: 20px;
        margin-bottom: 10px;
         cursor: pointer;
        padding: 8px;
        font-size: 20px;
        
    }
    .author {
        font-size: 16px;
        font-weight: 300;
        position: absolute;
        top: 50%;
        left: 15%;
    }
    .rotate {
        transform: translateX(-50%) translateY(-50%) rotate(90deg);
    }
    @media screen and (max-width: 800px) {
        .row {
            display: block;
        }
    }
</style>