#!/bin/bash/python


<form action = "{{ url_for('addrec') }}" method = "POST">
	<h3>Add a warehouse - </h3>
	Name<br>
	<input type = "text" name = "wh_name" /></br>

	Is_active<br>
	<input type = "text" name = "is_active" /></br>

	<input type = "submit" value = "submit" /><br>
</form>