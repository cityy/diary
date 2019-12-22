// oGraph constructor
function oGraph(containerId, settings){


    // 
    //  PROPERTIES
    // 
    ident = containerId;
    centerPoint = { x: 0, y: 0 };
    visNetwork = {};
    graphData = {
        nodes: {},
        edges: {}
    };
    regions = [];
    this.settings = {};
    defaultSettings = { 
    };


    //
    // INITIALIZATION
    //
    __init = function(oGraph){
        
        // check if there are custom settings, else use default settings
        settings ? oGraph.settings = settings : oGraph.settings = defaultSettings;

        // get the graph center point to determine region positions
        // IIEF: returns the window center coordinate as an array[x,y]
        centerPoint = function(){ 
            let w = Math.max( document.documentElement.clientWidth, window.innerWidth || 0 );
            let h = Math.max( document.documentElement.clientHeight, window.innerHeight || 0 );
            return { x: w/2, y: h/2 };
        }();

        // create a network
        graphData.nodes = new vis.DataSet([ { id: 1, label: 'center', x: centerPoint.x, y: centerPoint.y } ]);
        graphData.edges = new vis.DataSet([]);

        var options = {};

        var container = document.getElementById(containerId);
        visNetwork = new vis.Network(container, graphData, {});

    }(this);


    var redraw = function(){
        // computer region positions
            var regionNodes = graphData.nodes.get({
              filter: function (item) {
                return (item.type == 'region');
              }
            });
            
            360/regionNodes.length;

        visNetwork.redraw();
    }


    // 
    //  API FUNCTIONS
    // 

    // f: addRegion
    // api function to add a new Region to the graph
    // name can be a string or an array of strings
    this.addRegion = function( name, settings ){
        if( typeof( names ) === 'object' ){
            for( let n in name ){
                regions.push( new oRegion( n, graphData, centerPoint ) );
            }
        }
        else{
            regions.push( new oRegion( name, graphData, centerPoint ) );
        }
        redraw();
    } // f: addRegion




    // 
    //  CONSTRUCTORS
    //
    // region constructor
    function oRegion( regionName, graphData, centerPoint, settings ){
        // 
        // Properties
        // 
        // let parent = graphId;
        let name = regionName;
        let node
        let tracks = [];
        this.settings = {};
        let defaultSettings = {
            radius: 300,
        };

        // 
        // Initialization
        // 
        __init = function(oRegion){
            settings ? oRegion.settings = settings : oRegion.settings = defaultSettings;
            // how many regions are there?

             // track constructor
            function oTrrack(){}
            // entry constructor
            function oEntry(){}
            // console.log(network.nodes)
            // vis interaction
            graphData.nodes.add({ type: 'region', id: name, label: name, });
            // add node to graph
        }(this); // f: init
    } // f: oRegion constructor


}