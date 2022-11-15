document.querySelector('.trade-index-radio-form').addEventListener("click", function(){
    console.log(document.querySelector('.trade-index-radio-form'))
    var check_id = document.querySelector('input[name="trade"]:checked').id;
    var radios = document.getElementsByName('trade');
    
    for (var i=0; i<radios.length; i++)
    {
      // 체크된 라디오가 현재 인덱스의 id와 같다면
      // -> show
      if (check_id === String(i)) {
        document.querySelector('#trade-card-'+String(i)).setAttribute('style', '')
      }
      // 다르다면
      // -> hide
      else {
        document.querySelector('#trade-card-'+String(i)).setAttribute('style', 'display: none')
      }
    }
})