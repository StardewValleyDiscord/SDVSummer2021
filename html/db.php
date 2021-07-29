<?php
    define("DB_PATH", "/private/summer.db");

    function populate_leaderboard() {
        $db = new SQLite3(DB_PATH);
        $query = $db->prepare('SELECT * FROM teams ORDER BY points DESC');
        $ret = $query->execute();

        $rank = 0;
        while ($row = $ret->fetchArray()) {
            $rank += 1;
            $name = $row['team_name'];
            $pts = $row['points'];

            echo "<tr>";
            echo "<td class='team-rank'>$rank</td>";
            echo "<td class='team-name'>$name</td>";
            echo "<td class='team-pts'>$pts</td>";
            echo "</tr>";
        }

        $db->close();
    };
?>
