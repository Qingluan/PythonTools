$^I = "";
$name = shift @ARGV;
while (<>) {
	$_ = "" if m/^$name/;
	print;
}