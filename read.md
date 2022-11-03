 {% for dt in pre %}
                      {% set dat1 = dt.delivery_date %}
                      {% set text1 = dat1.strftime("%Y,%m,%d") %}
                      {% set d1 = text1.split(",") %}
                     {% set dat2 = datetime.datetime.now() %}
                      {% set text2 = dat2.strftime("%Y,%m,%d") %}
                      {% set d2 = text2.split(",") %}
                      {% set wid = d((d1[0]|int), (d1[1]|int), (d1[2]|int)) - d((d2[0]|int), (d2[1]|int), (d2[2]|int))  %}
                      {% set wid1 = wid.days %}
                     
                      {% if wid1 <=5 and wid1 >-1%}
                      <li>
                        <a href="#">
                          <i class="fa fa-exclamation-triangle text-red" aria-hidden="true"></i>Cow ID: {{dt.cow.cow_no}} => {{dt.delivery_date}}
                        </a>
                        </li>
                      {% else %}
                      
                      {% endif %}
                      {% endfor %}




                       <div class="col-md-6">
      <div class="box box-danger" style="height:462px;overflow: auto;">
        <div class="box-header">
          <span><i class="fa fa-exclamation-circle" aria-hidden="true"></i>  List of Cow Feed</span>
        </div>
          <div class="box-body">
            <div class="box-body">
              <div class="box-body table-responsive">
              <table class="table table-hover table-bordered">
                  <thead>
                      <tr>
                          <td>Stall Number</td>
                          <td>Salt</td>
                          <td>Glass</td>
                          <td>Water</td>
                      </tr>
                  </thead>
                  <tbody>
                    {% for dt in data %}
                    <tr>
                        <td>{{dt.stall_no}}</td>
                          {% for d,i in enumerate(dt.feed_item) %}
                          <td> 
                            {{dt.item_quantity[d]}} {{dt.unit[d]}}
                          </td>
                          <td>
                            {{dt.item_quantity[d]}}
                          </td>
                          
                             
                         </tr>
                          {% endfor %}
                       
                    {% endfor %}
                  
                  </tbody>
                </table>
              </div>
          </div>
      </div>
     </div>
     


     Diagram:
     1. Use case Diagram
     2. Use Case Description
     3. Activity Diagram
     4. Sequence Diagram
     5. Class Diagram
     6. ER-Diagram


     //Admin 
     