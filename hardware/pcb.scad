


PCB_LAYERS = [
    ["yellow", "production-files/motherboard-Edge_Cuts.svg"],
    ["red", "production-files/motherboard-F_Adhes.svg"],
    ["red", "production-files/motherboard-F_Cu.svg"],
    ["red", "production-files/motherboard-F_Mask.svg"],
    ["red", "production-files/motherboard-F_Paste.svg"],
    ["red", "production-files/motherboard-F_SilkS.svg"],
    
    //"production-files/motherboard-B_Adhes.svg",
    //"production-files/motherboard-B_Cu.svg",
    //"production-files/motherboard-B_Mask.svg",
    //"production-files/motherboard-B_Paste.svg",
    //"production-files/motherboard-B_SilkS.svg",
];

translate([-10,-30,14]) motherboard(use_layers="production-files/", $fn=60);
color("yellow") !mount($fn=60);



module motherboard(use_layers) {
    
    layers_imported = use_layers != "";
    
    color("green") linear_extrude(1.6) difference() {
        // Main board
        s = [160, 100];
        o = 2.5;
        square(s, true);
        for (p=[[s[0]/2-o,s[1]/2-o],[-s[0]/2+o,s[1]/2-o],[-s[0]/2+o,-s[1]/2+o],[s[0]/2-o,-s[1]/2+o]]) translate(p) circle(d=3);

        // Modules
        translate([-s[0]/2+30+6,-s[1]/2+32.5]) rotate([0,0,-90]) scale([1,-1,1]) rpi();
        translate([s[0]/2-28,s[1]/2-35]) rotate([0,0,90]) motor_esc();
        translate([-s[0]/2+22,s[1]/2-15]) rotate([0,0,90]) rtc();
               
        // Interface connectors
        *translate([0,-45]) {
            translate([-30, 0]) pinheader(5, 5.12, center=true);    // Power in           
            translate([5, 0]) pinheader(3, 5.12, center=true);      // Motor out
            translate([25, 0]) pinheader(5, 2.56, center=true);     // Motor Enc in
            translate([70, 0]) pinheader(4, 5.12, center=true);     // Audio out
        }       
    }
    
    if (layers_imported) translate([-180, -147, 1.6]) linear_extrude(0.01) color("red") import(str(use_layers, "motherboard-F_Cu.svg"));
    if (layers_imported) translate([-180, -147, -0.01]) linear_extrude(0.01) color("black") import(str(use_layers, "motherboard-B_Cu.svg"));
}


module motor_esc() {
    hl=57/2;
    hw=36.5/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    
    *translate([2.5,0]) square([hl*2-10, (hw)*2], true);
    
    translate([hl+.5, 0]) {
        translate([0,hw-4]) rotate([0,0,-90]) pinheader(6);
        translate([0,-hw+3]) rotate([0,0,90]) pinheader(5);
    }
    translate([-hl+1, 2-10]) rotate([0,0,90]) pinheader(5, 4, center=false);
}


module audio_amp() {
    hl=48.5/2;
    hw=28/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);
    //square([hl*2-6, hw*2+3], true);
    translate([hl+1,hw-5]) rotate([0,0,-90]) pinheader(2, 12.5, center=true);
}


module fan(size=40) {
    circle(d=size-2);
    hs=size/2 - 4;
    for (p=[[hs,hs], [hs,-hs], [-hs,-hs], [-hs,hs]]) translate(p) circle(d=3);
}


module rpi(fan=true) {
    hl=58/2;
    hw=49/2;
    for (p=[[hl,hw], [hl,-hw], [-hl,-hw], [-hl,hw]]) translate(p) circle(d=3);   
    translate([85/2-10,-30]) square([30, 60]);
    
    translate([0,hw+2.56/2]) pinheader(20, 2.54, center=true);
    translate([0,hw-2.56/2]) pinheader(20, 2.54, center=true);
    
    if (fan) translate([(-hl-3.5)+29,(hw+3.5)-26]) fan(40);
}


module rtc() {
    translate([0,34/2]) pinheader(6, center=true);
    translate([0,-34/2])pinheader(4, center=true);
}


module pinheader(n=1, spacing=2.54, center=false) {
    translate([-((n-1)*spacing/2)*bool2int(center), 0]) {
        for (i=[0:1:n-1]) translate([i*spacing, 0]) circle(d=1);
    }
}

function bool2int(state) = state ? 1 : 0;













/// **** MOUNTING **** ///
module mount() {
    pts = [
        // First corner
        [-70,40],
        [-70, 45-20],
        [-75-20, 45-20],
    
        // Second corner
        [-75-20, -50-30-20],
    
        // Third corner
        [60+20, -50-30-20],
    
        // Forth corner
        [60+20, 45-20],
        [70, 45-20],
        [70, 40]
    ]; 
    
    linear_extrude(3) difference() {
        polygon(pts);
        for (p=[[140/2,0], [-140/2,0]]) translate(p) circle(d=8);
        translate([0,-30]) circle(d=120);
    }
    
    linear_extrude(10) for (p=[[140/2,0], [-140/2,0]]) translate(p) difference() {
        circle(d=12);
        circle(d=8);
    }
    
    s = [160, 100];
    o = 2.5;
    translate([-14, -26])
    for (p=[[s[0]/2-o,s[1]/2-o],[-s[0]/2+o,s[1]/2-o],[-s[0]/2+o,-s[1]/2+o],[s[0]/2-o,-s[1]/2+o]]) translate(p) linear_extrude(14) difference() {
        circle(d=6);
        circle(d=3);
    }
    
}

