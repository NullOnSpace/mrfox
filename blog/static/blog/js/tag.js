var jqSetTag = $('#set-tag');

function closeModal() {
  $('.modal').css('display', 'none');
}

function refreshCurrentTagList() {
  window.currentTagList = new Array();
  $('.modal .tag-edit .current-tags span.tag').each(function(){
    currentTagList.push(this.innerText.trim());
  });
}

if (jqSetTag.length > 0) {
  // Click event to popup tag modal
  refreshCurrentTagList();
  jqSetTag.click(function(event) {
    $('.modal').css('display', 'block');
    $('.modal .modal-title .close').click(function(){
      closeModal();
    });
  });
  // Click event to add new tag
  $('.new-tag input:submit').click(function(e){
    var jqNewTagWrapper = $('.new-tag input[name="new-tag"]');
    var strNewTags = jqNewTagWrapper.val();
    jqNewTagWrapper.val("");
    // Get common tag list
    // var commonTagList = new Array();
    // $('.modal .tag-edit .canditate-tags span.tag').each(function(){
    //   commonTagList.push(this.innerText);
    // });
    // Handle input tags
    var tagList = strNewTags.split(" ");
    for (var i=0;i<tagList.length;i++) {
      var strTag = tagList[i].toLowerCase().trim();
      if (strTag) {
        var idx = currentTagList.indexOf(strTag.toLowerCase());
        if (idx == -1) {
          // Tag not in current tag, so it can be add
          // Create new tag span and add to current tags
          var eleTagSpan = document.createElement('span');
          eleTagSpan.classList.add('tag');
          eleTagSpan.innerText = strTag;
          var eleTagCloseSpan = document.createElement('span');
          eleTagCloseSpan.classList.add('close');
          eleTagCloseSpan.classList.add('del');
          eleTagSpan.appendChild(eleTagCloseSpan);
          $('.tag-edit .current-tags i').remove();
          $('.tag-edit .current-tags').append(eleTagSpan);
          // Add to current-tag-list to avoid following same tag.
          currentTagList.push(strTag);
        }
      }
    }
    e.preventDefault();
  });
  // Click event for remove a current tag
  $('.tag-edit .current-tags .tag .close.del').click(function(event){
    var eleCurrentTag = event.currentTarget.parentElement;
    var strTag = eleCurrentTag.innerText.trim();
    var idx = currentTagList.indexOf(strTag);
    if (idx == -1) {
      // tag not in tag list, this shouldn't happen
      console.log('rm tag error', idx, strTag);
    } else {
      currentTagList.splice(idx, 1);
      $(eleCurrentTag).remove()
    }
    event.preventDefault();
  });
  // Click event for tag submit
  $('input#tag-submit').click(function(event) {
    var jqSelectTags = $('select[name="tags"]');
    jqSelectTags.empty();
    for (var i=0;i<currentTagList.length;i++) {
      var strTag = currentTagList[i];
      var eleOptionTag = document.createElement('option');
      eleOptionTag.value = strTag;
      eleOptionTag.selected = true;
      jqSelectTags.append(eleOptionTag);
    }
    var eleFormTag = $('form#tag')[0];
    $.ajax({
      url: eleFormTag.action,
      type: 'POST',
      data: $(eleFormTag).serialize(),
      traditional: true,
      dataType: 'json',
      success: function(suda){
        // console.log(suda);
        var newTagObject = suda.tags;
        var jqSpanTags = $('p.tags > span.tags');
        jqSpanTags.empty();
        $.each(newTagObject, function(name, slug){
          var eleSpanTag = document.createElement('span');
          $(eleSpanTag).addClass('tag');
          var eleATagPostList = document.createElement('a');
          var eleSpanTagIcon = document.createElement('span');
          $(eleSpanTagIcon).addClass("glyphicon");
          $(eleSpanTagIcon).addClass("glyphicon-tag");
          eleATagPostList.innerText = name;
          eleATagPostList.href = postTagListURL.replace('tobereplaced', slug);
          $(eleATagPostList).prepend(eleSpanTagIcon);
          eleSpanTag.appendChild(eleATagPostList);
          jqSpanTags.append(eleSpanTag);
        });
      },
      complete: function(){
        closeModal();
      }
    });
    event.preventDefault();
  });
  // Click event for tag modal cancel
  $('div.tag-edit button').click(function(event){
    closeModal();
    event.preventDefault();
  });
}
