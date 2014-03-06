$^I = "";

$name =shift @ARGV;
$time = shift @ARGV;
while(<>){
	$_ = "$name    $time\n" if m/^\b$name\b/ ;
	print;
}
