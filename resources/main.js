
contentOffsetFull = 20;
contentOffsetHidden = 0;
contentOffset = contentOffsetFull;

function offsetContentsFn() {
  var height = $("#header-elt").height() + contentOffset + "px";
  $("#container-elt").css({ "margin-top": height });
};

function inIframe () {
  try {
      return window.self !== window.top;
  } catch (e) {
      return true;
  }
};


$(document).ready(function () {
  $(window)
    .resize(function () {
      if (!inIframe()) {
      offsetContentsFn();} else {
        window.addEventListener('message', function(e) {
          let message = e.data;
          if (message === 'ar') {
            $("#langs-menu").prop("value", "ar-EG").trigger('change');
          };
        } , false);
        $('#doc-abstract, #credits, #update-date, #hide-intro-container, #header-elt hr').css( "display", "none");
        $('#hide-defs-cb').prop("checked", false).trigger('change');
        $('#header-elt').css("position", "unset");
        $('#container-elt').css("margin-top", "unset");
        $('#container-elt').css("max-width", "unset");
        $('#header-elt').css("max-width", "unset");
        $('#header-elt').css( "width", "unset");
        $('#doc-title').css( "visibility", "hidden", "font-size", "0.5em");
        $('#langs-menu').css( "right", "0");
        $('#langs-menu').css( "margin-top", "0");

        contentOffsetFull = 0;
        contentOffsetHidden = 0;
        contentOffset = 0;
        // offsetContentsFn()
        console.log('showing definitions');
        let message = { height: document.body.scrollHeight + 30, width: document.body.scrollWidth };
        // window.top refers to parent window
        window.top.postMessage(message, "*");
        // console.log(message);
        console.log('loaded here');
      }
    })
    .trigger("resize");

  $(".term-en a")
    .attr("disabled", "disabled")
    .on("click", function () {
      return false;
    })
    .css({ color: "black", cursor: "default" });
    $('#hide-defs-cb').prop('checked','true').trigger('change');
    // testing
    // $('#langs').val('ar-EG').trigger('change')
    // $('#hide-intro-cb').prop('checked',true).trigger('change')
});

function hideIntro(cb) {
  var searchHeader = $("#search-header");
  var termsContainer = $("#terms-container");
  if (cb.checked) {
    contentOffset = contentOffsetHidden;
    $("#intro-part").addClass("hidden");
    offsetContentsFn();
    searchHeader.addClass("fixed-header");
    termsContainer.css("padding-top", searchHeader.height() + 10 + "px");
  } else if (!cb.checked) {
    contentOffset = contentOffsetFull;
    $("#intro-part").removeClass("hidden");
    searchHeader.removeClass("fixed-header");
    offsetContentsFn();
    termsContainer.css("padding-top", "0px");
  }
  window.scrollTo(0, 0);
};

function hideDefs(cb) {
  if (cb.checked) {
    $(".term-def-en").addClass("hidden");
    $(".term-definition-lang").addClass("hidden");
    $(".term-translation-note").addClass("hidden");
  } else if (!cb.checked) {
    $(".term-def-en").removeClass("hidden");
    $(".term-definition-lang").removeClass("hidden");
    $(".term-translation-note").removeClass("hidden");
  }
  window.scrollTo(0, 0);
};

function filterSources(v) {
  console.log(v);
  $(".glossary-term").removeClass("filtered-out");
  if (v != "0") {
    $(".glossary-term[data-source-group !=" + v + "]").addClass("filtered-out");
  }
};

function searchTerms(en = true) {
  // Declare variables
  var input, filter, allTerms, term, tNameClass, tNameElt, txtValue;
  input = document.getElementById(en ? "search-en-input" : "search-lang-input");
  filter = input.value.toLowerCase();
  allTerms = document.getElementById("terms-container");
  terms = allTerms.querySelectorAll(".glossary-term");
  tNameClass = en ? "term-name-en" : "term-name-lang";

  // Loop through all list items, and hide those who don't match the search query
  for (i = 0; i < terms.length; i++) {
    tNameElt = terms[i].getElementsByClassName(tNameClass)[0];
    txtValue = tNameElt.dataset.termName;
    if (txtValue.toLowerCase().indexOf(filter) > -1) {
      terms[i].classList.remove("searched-out");
    } else {
      terms[i].classList.add("searched-out");
    }
  }
};

function sortFunc(s, e) {
  var tNameClass, allTerms, terms, v, removeArrow, arrow;
  tNameClass = s ? "term-name-en" : "term-name-lang";
  allTerms = document.getElementById("terms-container");
  terms = Array.prototype.slice.call(
    allTerms.querySelectorAll(".glossary-term")
  );
  v = e.dataset.sorted;
  removeArrow = "null";
  arrow = "null";
  switch (v) {
    case "0":
      console.log("case 0");
      removeArrow = "fa-sort";
      terms.sort(function (a, b) {
        var name_a = a
          .getElementsByClassName(tNameClass)[0]
          .dataset.termName.toLowerCase();
        var name_b = b
          .getElementsByClassName(tNameClass)[0]
          .dataset.termName.toLowerCase();
        if (name_a > name_b) return 1;
        if (name_a < name_b) return -1;
        return 0;
      });
      arrow = "fa-sort-down";
      e.dataset.sorted = 1;
      break;
    case "1":
      console.log("case 1");
      removeArrow = "fa-sort-down";
      terms.reverse();
      arrow = "fa-sort-up";
      e.dataset.sorted = -1;
      break;
    case "-1":
      console.log("case -1");
      removeArrow = "fa-sort-up";
      terms.sort(function (a, b) {
        var name_a = a.dataset.index;
        var name_b = b.dataset.index;
        return name_a - name_b;
      });
      arrow = "fa-sort";
      e.dataset.sorted = 0;
      break;
  }
  for (let i = 0; i < terms.length; i++) {
    document.getElementById("terms-container").appendChild(terms[i]);
  }
  e.getElementsByTagName("i")[0].classList.remove(removeArrow);
  e.getElementsByTagName("i")[0].classList.add(arrow);
};

function changeLangIntro(lang, intro, direction) {
  document.dir = ["rtl", "ltr"].includes(direction) ? direction : "auto";
  hide_cb = document.getElementById("hide-intro-cb").checked;
  hide_cb2 = document.getElementById("hide-defs-cb").checked;
  selector = document.getElementById("langs-menu").cloneNode(true);
  selector2 = document.getElementById("langs").cloneNode(true);
  selector3 = document.getElementById("credits").cloneNode(true);
  selector3.dir = direction
  if (lang.startsWith('ar-')) {
    $(selector3).find('h4').text(allLangs["langs"]["ar-EG"]["translated-by"][0]["name"][1]);
  } else { 
    $(selector3).find('h4').text(allLangs["langs"]["ar-EG"]["translated-by"][0]["name"][0]);
  }
  selector4 = document.getElementById("update-date").cloneNode(true);
  selector4.innerText = new Date(selector4.dataset.updated).toLocaleDateString(lang, {month:'long', year:'numeric'})

  header = `
    <header id="header-elt" class="fixed-header">
            <div id='header-first' style="position: relative;">
                <h1 id="doc-title" class="title" lang="${lang}">${
    intro["doc-title"][lang] || intro["doc-title"]["en"]
  }</h1>
            </div>
            <div>
                <p id="doc-abstract" class="abstract" lang="en">
                    ${
                      intro["doc-abstract"][lang] || intro["doc-abstract"]["en"]
                    }
                </p>
            </div>
            <div id="credits"></div>
            <h5 id="update-date"></h5>
            <div id="hide-intro-container">
                <input type="checkbox" id="hide-intro-cb" name="hide-intro-cb" onchange="hideIntro(this)">
                <label id="label-hide-intro-cb" for="hide-intro-cb">${
                  intro["label-hide-intro-cb"][lang] ||
                  intro["label-hide-intro-cb"]["en"]
                }</label>
            </div>
            <hr style="margin-bottom: 0; min-width: 720px;">
        </header>
    `;

  intro_part = `
    <div id="intro-part">
    <div id="about-section">
        <h3 id="about-title">${
          intro["about-title"][lang] || intro["about-title"]["en"]
        }</h3>
        <p id="about-para-1">${
          intro["about-para-1"][lang] || intro["about-para-1"]["en"]
        }</p>
        <p id="about-para-2">${
          intro["about-para-2"][lang] || intro["about-para-2"]["en"]
        }</p>
        <p id="sources-used-title">${
          intro["sources-used-title"][lang] || intro["sources-used-title"]["en"]
        }</p>
        <ul>
            <li>
                <p>
                    <a id="sources-li-1-1" href="https://xbrl.us/xbrl-reference/tdh/" target="_blank">${
                      intro["sources-li-1-1"][lang] ||
                      intro["sources-li-1-1"]["en"]
                    }</a>
                    <span id="sources-li-1-2">${
                      intro["sources-li-1-2"][lang] ||
                      intro["sources-li-1-2"]["en"]
                    }</span>
                    <a href="https://xbrl.us/" target="_blank">XBRL US:</a>
                    <span id="sources-li-1-3">${
                      intro["sources-li-1-3"][lang] ||
                      intro["sources-li-1-3"]["en"]
                    }</span>
                </p>
            </li>
            <li>
                <p>
                    <a href="https://www.xbrl.org/guidance/xbrl-glossary/" target="_blank">XBRL Glossary</a>
                    <span id="sources-li-2-1">${
                      intro["sources-li-2-1"][lang] ||
                      intro["sources-li-2-1"]["en"]
                    }</span>
                    <a href="https://www.xbrl.org" target="_blank">XBRL International:</a>
                    <span id="sources-li-2-2">${
                      intro["sources-li-2-2"][lang] ||
                      intro["sources-li-2-2"]["en"]
                    }</span>
                </p>
            </li>
            <li>
                <p>
                    <a id="sources-li-3-1" href="https://www.sec.gov/page/osd_xbrlglossary" target="_blank">${
                      intro["sources-li-3-1"][lang] ||
                      intro["sources-li-3-1"]["en"]
                    }:</a>
                    <span id="sources-li-3-2">${
                      intro["sources-li-3-2"][lang] ||
                      intro["sources-li-3-2"]["en"]
                    }</span>
                </p>
            </li>
            <li>
                <p>
                    <a id="sources-li-4-1" href="https://specifications.xbrl.org/specifications.html" target="_blank">${
                      intro["sources-li-4-1"][lang] ||
                      intro["sources-li-4-1"]["en"]
                    }:</a>
                    <span id="sources-li-4-2">${
                      intro["sources-li-4-2"][lang] ||
                      intro["sources-li-4-2"]["en"]
                    }</span>
                    </p>
                </li>
            </ul>
        </div>
        <div id="translations">
            <h3 id="translation-section-title">${
              intro["translation-section-title"][lang] ||
              intro["translation-section-title"]["en"]
            }</h3>
            <p><span id="translation-section-1">${
              intro["translation-section-1"][lang] ||
              intro["translation-section-1"]["en"]
            }</span> 
                <a id="translation-section-2" href="#lang-menu">${
                  intro["translation-section-2"][lang] ||
                  intro["translation-section-2"]["en"]
                }</a> 
                <span id="translation-section-3">${
                  intro["translation-section-3"][lang] ||
                  intro["translation-section-3"]["en"]
                }</span>
                <a id="translation-section-4" href="https://github.com/selgamal/xbrl-glossary-collection" target="_blank">${
                  intro["translation-section-4"][lang] ||
                  intro["translation-section-4"]["en"]
                }</a> 
                <span id="translation-section-5">${
                  intro["translation-section-5"][lang] ||
                  intro["translation-section-5"]["en"]
                }</span>
            </p>
            </div>
        <div id="notes-on-translation-for-language" class="hidden">
            <h3 id="lang-notes-section-title" >${
              intro["lang-notes-section-title"][lang] ||
              intro["lang-notes-section-title"]["en"]
            }</h3>
            <p id="lang-notes-section-text">${
              intro["lang-notes-section-text"][lang] ||
              intro["lang-notes-section-text"]["en"]
            }</p>
        </div>
        <div id="glossary">
            <h3 id="glossary-section-title">${
              intro["glossary-section-title"][lang] ||
              intro["glossary-section-title"]["en"]
            }</h3>
            <p id="glossary-section-1">${
              intro["glossary-section-1"][lang] ||
              intro["glossary-section-1"]["en"]
            }</p>
            <p id="glossary-section-2">${
              intro["glossary-section-2"][lang] ||
              intro["glossary-section-2"]["en"]
            }</p>
        </div>
    </div>
    `;

  search_bar = `
    <div id="search-header">
                        <div id="search-container">
                            <button id="sort-en" data-sorted="0" type="sort" onclick="sortFunc(true, this)" title="${
                              intro["title-8"][lang] || intro["title-8"]["en"]
                            }">
                                <i class="fa fa-sort"></i>
                            </button>
                            <select name="all" id="select-sources" title="${
                              intro["title-6"][lang] || intro["title-6"]["en"]
                            }" onchange="filterSources(this.value)">
                                <option value="0" selected>All</option>
                                <option value="1">XBRL Specifications</option>
                                <option value="2" title="XBRL Taxonomy Development Handbook">TDH</option>
                                <option value="3">XBRL.org Glossary</option>
                                <option value="4" >SEC Glossary</option>
                            </select>
                            <form id="hide-defs-container">
                            <input type="checkbox" id="hide-defs-cb" name="hide-defs-cb" onchange="hideDefs(this)">
                            <label id="label-hide-defs-cb" for="hide-defs-cb">${
                              intro["label-hide-defs-cb"][lang] ||
                              intro["label-hide-defs-cb"]["en"]
                            }</label>
                          </form>
                            <form  id="search-en" style="display: flex;" title="${
                              intro["title-2"][lang] || intro["title-2"]["en"]
                            }" onkeyup="searchTerms()">
                                <input type="text" id="search-en-input" placeholder="${
                                  intro["placeholder-1"][lang] ||
                                  intro["placeholder-1"]["en"]
                                }" name="search-en-input">
                            </form>
                            <form  id="search-lang" style="display: flex;" title="${
                              intro["title-3"][lang] || intro["title-3"]["en"]
                            }" onkeyup="searchTerms(false)"  dir="${direction}">
                                <input type="text" id="search-lang-input" placeholder="${
                                  intro["placeholder-2"][lang] ||
                                  intro["placeholder-2"]["en"]
                                }" name="search-lang-input">
                            </form>
                            <button id="download-button" dir="${direction}" type="download" title="${
    intro["title-7"][lang] || intro["title-7"]["en"]
  }" onclick="makeLangsFile()">
  <!-- <a href="https://github.com/selgamal/xbrl-glossary-collection/blob/master/json/all-langs.json" style="color: black;"target="_blank">  -->
                                    <i class="fa fa-download">
                                    </i>
                                </a>
                            </button>
                            <button id="sort-lang" data-sorted="0" type="sort" onclick="sortFunc(false, this)" title="${
                              intro["title-9"][lang] || intro["title-9"]["en"]
                            }">
                                <i class="fa fa-sort"></i>
                            </button>
                        </div>
                        <hr style="margin-bottom: 0;">
                    </div>
    `;

  newHeader = document.createElement("template");
  newHeader.innerHTML = header;
  document.getElementById("header-elt").replaceWith(newHeader.content);
  document
    .getElementById("doc-title")
    .insertAdjacentElement("afterend", selector);

  newIntro = document.createElement("template");
  newIntro.innerHTML = intro_part;
  document.getElementById("intro-part").replaceWith(newIntro.content);

  newSearch = document.createElement("template");
  newSearch.innerHTML = search_bar;
  document.getElementById("search-header").replaceWith(newSearch.content);
  document
    .getElementById("sort-en")
    .insertAdjacentElement("afterend", selector2);
  
  document.getElementById('credits').replaceWith(selector3)
  document.getElementById('update-date').replaceWith(selector4)
  //clean up
  $("#langs-menu").val(lang);
  $("#hide-intro-cb").attr({ checked: hide_cb }).change();
  $("#hide-defs-cb").attr({ checked: hide_cb2 }).change();
  if (lang.toLowerCase().startsWith('en')) {
      $('#notes-on-translation-for-language').addClass('hidden')
  } else {
  $('#notes-on-translation-for-language').removeClass('hidden')
}
};

function showLangTerms(lang) {
  var glossary, terms, classes, term_lang, innerElt, inner_text;
  glossary = allLangs;
  classes = [
    "term-name-lang",
    "term-name-lang-variants",
    "term-definition-lang",
    "translation-notes",
  ];
  terms = $(".glossary-term");
  trans_note = glossary["intro"]["trans-note"][lang];
  terms.find("#trans-note").text(trans_note.length > 0 ? trans_note : "--");
  for (let i = 0; i < terms.length; i++) {
    const element = terms[i];
    id = element.id;
    data = glossary["glossary"][id][lang];
    term_lang = $(element).find(".term-lang");
    if (data["term-name-lang"].length > 0) {
      term_lang.removeClass("empty-translation");
    }
    term_lang.attr({ dir: glossary["langs"][lang]["dir"], lang: lang });
    classes.map(function (x) {
      innerElt = $(term_lang).find("." + x);
      inner_text = data[x];
      if (inner_text.length == 0) {
        inner_text = x == "term-name-lang-variants" ? "[--]" : "--";
      } else {
        inner_text =
          x == "term-name-lang-variants"
            ? "[" + data[x].join("-") + "]"
            : data[x];
      }
      x == "term-definition-lang" ? innerElt.html(inner_text) : innerElt.text(inner_text);
      innerElt.attr({ lang: lang });
      if (x == "term-name-lang") {
        innerElt[0].dataset.termName = inner_text;
      }
    });
  }
};

function showTranslatedTerms(lang) {
  if (lang == "en") {
    $(".term-lang").addClass("hidden");
  } else {
    showLangTerms(lang);
    $(".term-lang").removeClass("hidden");
  }
};

function makeLangsFile() {
  var blob = new Blob([JSON.stringify(allLangs, null, 2)], {type: "application/json;charset=utf-8"});
  var url = URL.createObjectURL(blob);
  var elem = document.createElement("a");
  elem.id = 'temp-link';
  elem.href = url;
  elem.target = '_blank';
  elem.download='all-langs.json'
  elem.click()
}

function changeLangAll(menu) {
  var selectedValue;
  selectedValue = menu.value;
  direction = allLangs["langs"][selectedValue]["dir"];
  intro = allLangs["intro"];
  changeLangIntro(selectedValue, intro, direction);
  $("#langs").val(selectedValue).change();
  $(window).trigger("resize");
};
