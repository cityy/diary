var init = function(){

		// scroll beyond filters
		setTimeout(function () {
            window.scrollTo(0, 600);
        },1);

	var filterTags = document.getElementsByClassName('filterTag');
	var dictEntries = document.getElementsByClassName('dictWord');
	var dictLetters = document.getElementsByClassName('dictLetter');
	var activeFilters = {};
	var filterCount = 0;


	var applyFilter = function(){
		console.log(activeFilters);
		for(let j = 0; j<dictEntries.length;j++){
			if(filterCount > 0){
				dictEntries[j].style.display = 'none';
				for (var property in activeFilters) {
					if (activeFilters.hasOwnProperty(property)) {
						for(let k = 0; k < activeFilters[property].length; k++){
							if(dictEntries[j].getAttribute(property).includes(activeFilters[property][k])){
								dictEntries[j].style.display='block';
							}
							else if(dictEntries[j].style.display != 'block'){
								dictEntries[j].style.display = 'none';
							}
						}
					}
				}
			}
			else{
				dictEntries[j].style.display='block';
			}
		}
	}

	var filterTypes = [];
	for(let i=0; i<filterTags.length; i++){
		filterTypes.push(filterTags[i].getAttribute('type'))
	}
	filterTypes = filterTypes.reduce(function(a,b){
		if (a.indexOf(b) < 0 ) a.push(b);
		return a;
	},[]);
	for(let i=0;i<filterTypes.length;i++){
		activeFilters[filterTypes[i]] = [];
	}

	var toggleListView = function(){
		if(document.getElementById('listViewToggle').classList.contains('active') == false){
			document.getElementById('dictFilter').classList.add('col-24');
			for(let i=0; i<dictEntries.length;i++){
				dictEntries[i].classList.add('col-6');
			}
			for(let i=0; i<dictLetters.length;i++){
				dictLetters[i].classList.add('col-24');
			}
			document.getElementById('listViewToggle').classList.add('active');
			document.getElementById('fieldViewToggle').classList.remove('active');
		}
		else{
			document.getElementById('dictFilter').classList.remove('col-24');
			for(let i=0; i<dictEntries.length;i++){
				dictEntries[i].classList.remove('col-6');
			}
			for(let i=0; i<dictLetters.length;i++){
				dictLetters[i].classList.remove('col-24');
			}
			document.getElementById('listViewToggle').classList.remove('active');
			document.getElementById('fieldViewToggle').classList.add('active');
		}
	}

	document.getElementById('listViewToggle').addEventListener('click', function(){ toggleListView(); });
	document.getElementById('fieldViewToggle').addEventListener('click', function(){ toggleListView(); });
	window.addEventListener('keydown', function(e){
		e.keyCode == 76 ? toggleListView() : null;
	});


	for(let i=0; i<filterTags.length; i++){
		// console.log(filterTags[i].getAttribute('type'))
		// console.log(filterTags[i])
		filterTags[i].addEventListener('click', function(e){
			if(this.classList.contains('active') == false){
				this.classList.add('active');
				activeFilters[this.getAttribute('type')].push(this.getAttribute('value'));
				filterCount++;
				applyFilter();
			}
			else{
				this.classList.remove('active');
				let index = activeFilters[this.getAttribute('type')].indexOf(this.getAttribute('value'));
				activeFilters[this.getAttribute('type')].splice(index,1);
				filterCount--;
				applyFilter();
			}
		});
	}

	var getParentByClass = function(elem, className){
		let child = elem;
		let cn = '';
		let parent = '';
		while(!cn.includes(className)){
			cn = child.parentElement.className;
			child = child.parentElement;
			if(!cn.includes(className)){
				parent = child.parentElement;
			}
		}
		return parent;
	};

	var getChildByClass = function(elem, className){
		let cn = '';
		let child = '';
		let currentChildren = parent.children;
		let loopChildren = function(parent){
			for(let p = 0; p < parent.length; p++){
				for(let i = 0; i<parent.children.length;i++){
					if(parent.children[i].className.includes(className)){
						return parent.children[i]
					}
				}
			}
			parent = parent.children;
			loopChildren(parent);
		}

		return loopChildren(elem);
	}

	window.addEventListener('click', function(e){
		//console.log(e.target)
		if(e.target.tagName == 'IMG'){
			let parent = getParentByClass(e.target, 'dictWord');
			//console.log(getChildByClass(parent, ''))
			if(parent.className.includes('activeCol')){
				parent.classList.remove('activeCol');
				e.target.parentElement.style.maxHeight = '500px';
			}
			else{
				parent.classList.add('activeCol');
				e.target.parentElement.style.maxHeight = '1000px';
				console.log(e.target.parentElement);
			}
		}
	});
}

window.addEventListener('load', init);