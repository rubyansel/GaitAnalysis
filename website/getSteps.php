<?php
$file = trim($_GET["file"]);
system('cat ../ml_model/'.$file, $o);
?>
