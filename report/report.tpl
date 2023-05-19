<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/latest/css/bootstrap.min.css">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.3.1/styles/default.min.css">
	<style>
		body {
			background-color: #f8f9fa;
			padding: 20px;
			font-family: Arial, sans-serif;
		}

		.table-wrapper {
			max-width: 100%;
			margin: 0 auto;
			overflow-x: auto;
		}

		table {
			width: max-content;
			min-width: 100%;
			border-collapse: collapse;
			border-spacing: 0;
		}

		th,
		td {
			padding: 10px;
			text-align: left;
			white-space: pre-wrap;
			word-break: break-word;
			border: none;
		}

		th {
			background-color: #343a40;
			color: #fff;
			font-weight: bold;
		}

		tbody tr:nth-child(even) {
			background-color: #f2f2f2;
		}

		.extra-info {
			display: none;
			padding: 10px;
			border-radius: 5px;
			margin-top: 10px;
			background-color: #fff;
			box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		}

		.extra-info pre code {
			display: block;
			padding: 10px;
			overflow-x: auto;
			background-color: #f8f9fa;
			border: 1px solid #dee2e6;
		}

		.footer {
			background-color: #343a40;
			color: #fff;
			padding: 10px;
			text-align: center;
			position: fixed;
			bottom: 0;
			left: 0;
			width: 100%;
		}

		.footer a {
			color: #fff;
			text-decoration: none;
		}
	</style>
</head>

<body>
	<div class="table-wrapper">
		<table class="table table-striped table-bordered table-hover">
			<thead class="thead-dark">
				<tr>
					<th>越权接口</th>
					<th>原始请求</th>
					<th>原始响应</th>
					<th>攻击请求</th>
					<th>攻击响应</th>
				</tr>
			</thead>
			<tbody>
				<!-- TRTRTR -->
			</tbody>
		</table>
	</div>

	<div class="footer">
		<p>© 2022 越权漏洞检测系统</p>
		<p>Powered By <a href="https://www.gem-love.com">颖奇L'Amore</a></p>
	</div>

	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
	<script>
		$(document).ready(function () {
			$(".extra-info").hide();
			$("tr:even").hide();
			$("tr:first").show();
			$("tr").click(function () {
				let tr = $(this).next("tr");
				let flag = 0;

				if (!tr.is(":visible")) {
					tr.show();
					flag = 1;
				}

				tr.find(".extra-info").slideToggle(function () {
					if (flag === 0 && tr.is(":visible")) {
						tr.hide();
					}
				});
			});

			$(".extra-info pre code").each(function () {
				var content = $(this).text();
				var formattedContent = formatTextContent(content);
				$(this).html(formattedContent);
			});
		});

		function formatTextContent(content) {
			var maxLength = 50; // 设置每行的最大长度
			var formattedContent = '';
			var lines = [];
			var line = '';
			var words = content.split(' ');
			for (var i = 0; i < words.length; i++) {
				line += words[i] + ' ';
				if (line.length >= maxLength) {
					lines.push(line);
					line = '';
				}
			}
			if (line !== '') {
				lines.push(line);
			}
			formattedContent = lines.join('<br>');
			return formattedContent;
		}
	</script>
</body>