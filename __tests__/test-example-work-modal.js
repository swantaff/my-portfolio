import React from 'react';
import {shallow} from 'enzyme';
import ExampleWorkModal from '../js/example-work-modal';


import Enzyme from 'enzyme';
import Adaptor from 'enzyme-adapter-react-16';

Enzyme.configure({adapter: new Adaptor()});

const myExample = {
    'title': "Work Example",
    'href' : "https://example.com",
    'desc' : "Consectetur quis nulla id ut esse enim eu fugiat irure duis aute.",
    'image':{
        'desc': "example screenshot of a project involving code",
        'src': "images/example1.png",
        'comment': ""
    }
};

describe("ExampleWorkModal component", () => {

    let component = shallow(<ExampleWorkModal example={myExample}
        open={false}/>);

    let openComponent = shallow(<ExampleWorkModal example={myExample}
        open={true}/>);
  
    let anchors = component.find("a");
 
    it("Should contain a single 'a' element", () => {
        expect(anchors.length).toEqual(1);
    });

    it("Should link to our project", () => {

       expect(anchors.prop('href')).toEqual(myExample.href);
    });

    it("Should have the modal class set correctlty", () => {
 
        expect(component.find(".background--skyBlue").hasClass("modal--closed")).toBe(true);
        expect(openComponent.find(".background--skyBlue").hasClass("modal--open")).toBe(true);
      
     });
});