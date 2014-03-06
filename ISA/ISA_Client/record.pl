open HISTORY, ">>./HISTORY.info" or die("unknow error ! $!\n");
$line = shift @ARGV;
while (<HISTORY>) {
	die() if m/$line/ ;
}

select HISTORY;
print "$line\n";
select STDOUT;