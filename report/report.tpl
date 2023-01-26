<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/latest/css/bootstrap.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/latest/js/bootstrap.min.js"></script>
    <style>
      table th, table td {
        width: 15%; 
      }
    </style>
</head>

<body>
  <div class="table-responsive">
    <table class="table table-striped table-bordered table-hover ">
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

      <div style="display: flex; justify-content: center; align-items: center; position: fixed; bottom: 0; width: 100%;">
        Copyright © 2022 越权漏洞检测系统
        Powered By <a href="https://www.gem-love.com">颖奇L'Amore</a>
      </div>
      
      <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
      <script>
      $(document).ready(function(){
        $(".extra-info").hide(); 
        $("tr").click(function(){
          $(this).next().find(".extra-info").slideToggle();
        });
      });
      </script>
      
</body>
