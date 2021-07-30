<!DOCTYPE html>
<html>
    <head>
        <title>SDV Summer 2021</title>
        <meta charset="utf-8">
        <link rel="icon" href="assets/cojiro.png" type="image/png">
        <link rel="stylesheet" href="css/leaderboard.css" type="text/css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">

        <meta property="og:title" content="SDV Summer 2021 Event Leaderboard" />
        <meta property="og:url" content="https://summer2021.stardew.chat/" />
        <meta property="og:image" content="/assets/" />
    </head>
    <body>
        <header>
            <h1>SDV Summer 2021 Event Leaderboard</h1>
        </header>
        <main>
            <table>
                <?php
                    include 'db.php';
                    populate_leaderboard();
                ?>
            </table>
        </main>
    </body>
</html>
