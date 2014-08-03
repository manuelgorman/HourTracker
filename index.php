<HTML>
<HEAD>
	<Title>Hours you're working</title>
	<style>
	body{
	text-align:center;
	background:url('http://images.manuelgorman.co.uk/img/tweed.png');
	font-family:sans-serif;
	}
	.newline{display:block;}
	.B{display:block;}
	#Earned,#start,#duration,#end,#susan{font-size:20px;display:inline-block;margin-top:1%;background-color:rgba(40, 40, 40, 0.4);padding:2px;margin-left:4px;margin-right:4px;color:#777777;margin-top:20px;}
	h1{color:#AAAAAA;text-decoration:underline;padding-bottom:2%;font-size:50px;}
	div{border-radius:5px;}
	#day,#date{
	display:inline;
	margin:auto;
	padding:1%;
	color:#888888;
	font-weight:bolder;
	font-size:40px;
	background-color:rgba(50,50,50, 0.3);
	}
	table{color:#888888;text-align:center;margin:auto;background-color:rgba(40,40,40,0.4);border-radius:10px;padding:5px;}
	#day{margin-right:2%;}
	#date{margin-left:2%;}
	h2{color:#AAAAAA;text-decoration:underline;font-size:20px;margin-top:5%}
	#bottom{font-weight:bolder;text-align:center;}
	.hover{transition-property:all;transition-duration:0.2s}
	.hover:hover{box-shadow: 0 0 3px 4px rgba(40,40,40,1);background-color:rgba(40,40,40,1)!important;}
	</style>
</HEAD>
<body>
<h1>Next Shift</h1>
<div>
<?php
exec('/usr/lib/cgi-bin/apps/hours/most_recent.py',$input);
foreach ($input as $value){echo $value;}


?>
</div>

<h2>Next 5 upcoming shifts</h2>
<?php
	exec('/usr/lib/cgi-bin/apps/hours/newNext5.py',$input2);
	foreach ($input2 as $value2){echo $value2;}
?>
</body>


</HTML>
