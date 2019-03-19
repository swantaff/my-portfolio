import React from 'react';
import {shallow} from 'enzyme';
import ExampleWork, {ExampleWorkBubble} from '../js/example-work';


import Enzyme from 'enzyme';
import Adaptor from 'enzyme-adapter-react-16';

Enzyme.configure({adapter: new Adaptor()});

// some test data for the component
const myWork = [
    {
        'title': "Work Example",
        'image':{
            'desc': "example screenshot of a project involving code",
            'src': "images/example1.png",
            'comment': ""
        }
    },
    {
        'title': "Portfolio Boilerplate",
        'image':{
            'desc': "A Serverless Portfolio",
            'src': "images/example2.png",
            'comment': ""
        }
    }
];

describe("ExampleWork component", () => {

    let component = shallow(<ExampleWork work={myWork}/>);
    
    it("Should be a 'span' element", () => {
       // console.log(component.debug());

       expect(component.type()).toEqual('span');
    });

    it("Should contain as many children as there are work examples", () => {
        expect(component.find("ExampleWorkBubble").length).toEqual(myWork.length);
    });
    
    it("Should allow the modal to open and close", () => {
        // call openModal fn
        component.instance().openModal();
        expect(component.instance().state.modalOpen).toBe(true);
        // call closeModal fn
        component.instance().closeModal();
        expect(component.instance().state.modalOpen).toBe(false);
    });

});

describe("ExampleWorkBubble component", () => {
    let mockOpenModalFn = jest.fn();

    let component = shallow(<ExampleWorkBubble example={myWork[1]}
        openModal={mockOpenModalFn} />)

    let images = component.find("img");

    it("Should contain a single 'img' element", () => {
        expect(images.length).toEqual(1);
    });

    it("Should have the image src set correctlty", () => {
        expect(images.prop('src')).toEqual(myWork[1].image.src);
    });

    it("Should call the openModal handler when clicked", () => {
        
        component.find(".section__exampleWrapper").simulate('click');
        expect(mockOpenModalFn).toHaveBeenCalled;
    });
});