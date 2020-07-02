<html>
<body>
<form action="index.php" method="post">
　Motion: <input type="test" name="Motion">
　<input type="submit" name="readybutton" value="Ready?">
</form>
</body>
</html>


<?php
// Set the fields that needed to be saved
$fields = array("name", "ax0", "ay0", "az0", "gx0", "gy0", "gz0", "ax1", "ay1", "az1", "gx1", "gy1", "gz1", "ax2", "ay2", "az2", "gx2", "gy2", "gz2", "ax3", "ay3", "az3", "gx3", "gy3", "gz3"/*, "ax4", "ay4", "az4", "gx4", "gy4", "gz4", "ax5", "ay5", "az5", "gx5", "gy5", "gz5"*/);
// Check the login information
$modules = fopen("./module_name.txt", "r");
$login = 0;
$pre_file = './module_data_';

while (!feof($modules)) {
/*	ob_start();
	var_dump($_POST);
	$dataa = ob_get_clean();
 */	$data = fopen("./gait/data.csv", "a");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields as $field) {
		fputs($data, ",");
		fputs($data, trim($_POST[$field]));
	}
	fputs($data, "\n");
//	fputs($data, $dataa);
//	fputs($data, "\n");
	fclose($data);
	$user = fgets($modules);
	$pwd = fgets($modules);
	if (trim($user) and !strcmp(trim($user), trim($_POST["name"]))) {
		if (trim($pwd) and !strcmp(trim($pwd), trim($_POST["password"])))
			$login = 1;
	}
}
fclose($module);

$fields1 = array("name", "ax0", "ay0", "az0", "gx0", "gy0", "gz0");
$fields2 = array("name", "ax1", "ay1", "az1", "gx1", "gy1", "gz1");
$fields3 = array("name", "ax2", "ay2", "az2", "gx2", "gy2", "gz2");
$fields4 = array("name", "ax3", "ay3", "az3", "gx3", "gy3", "gz3");
$fields5 = array("name", "ax4", "ay4", "az4", "gx4", "gy4", "gz4");
$fields6 = array("name", "ax5", "ay5", "az5", "gx5", "gy5", "gz5");

$modulename = $_POST['Name'];
$motion = $_POST['Motion'];
$ready = $_POST['readybutton'];
if ($ready) {
	$file = $pre_file.trim("left");
	$data = fopen($file, "a");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields1 as $fields) {
		if ($fields == "name") {
			fputs($data, ",");
			fputs($data, $motion);
		} else {
			fputs($data, ",");
			fputs($data, "0");
		}
	}
	fputs($data, "\n");
	fclose($data);
	$file = $pre_file.trim("right");
	$data = fopen($file, "a");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields1 as $fields) {
		if ($fields == "name") {
			fputs($data, ",");
			fputs($data, $motion);
		} else {
			fputs($data, ",");
			fputs($data, "0");
		}
	}
	fputs($data, "\n");
	fclose($data);
}
// Print the information about login
if ($login) {
	echo "Hi, welcome back.";
	$file = $pre_file.trim($_POST["name"]);
	$data = fopen($file, "a");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields1 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields2 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields3 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields4 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	/*
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields5 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	fputs($data, date("Y-m-d H:i:s"));
	foreach ($fields6 as $field) {
		fputs($data, ",");
		$dat = trim($_POST[$field]);
		$dat = strval($dat);
		fputs($data, $dat);
	}
	fputs($data, "\n");
	 */
	fclose($data);
} else
	echo "I do not know you.";
system('bash preprocess.sh', $o);
?>
