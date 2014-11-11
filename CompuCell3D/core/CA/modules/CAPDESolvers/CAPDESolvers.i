// -*-c++-*-


%module ("threads"=1) CAPDESolvers

//enables better handling of STL exceptions
%include "exception.i"
// C++ std::string handling
%include "std_string.i"

// C++ std::map handling
%include "std_map.i"

// C++ std::map handling
%include "std_set.i"

// C++ std::map handling
%include "std_vector.i"

%include "stl.i"


%import "../../../CAPython/CoreObjects.i"
//%import "../CoreObjects.i"


%include "typemaps.i"

// ************************************************************
// Module Includes 
// ************************************************************

// These are copied directly to the .cxx file and are not parsed
// by SWIG.  Include include files or definitions that are required
// for the module to build correctly.
//DOCSTRINGS



%include <windows.i>

%{
// CompuCell3D Include Files
//#include <CompuCell3D/Field3D/Point3D.h>
//#include <CompuCell3D/Field3D/Dim3D.h>

#include <CompuCell3D/Field3D/Array3D.h>
#include <CA/modules/CAPDESolvers/DiffSecrData.h>
#include <CA/modules/CAPDESolvers/DiffusionSolverFE.h>



// Namespaces
using namespace std;
using namespace CompuCell3D;



%}




//////%include stl.i //to ensure stl functionality 
//////
//////// // // %include "CompuCellExtraIncludes.i"
//////
//////// C++ std::string handling
//////%include "std_string.i"
//////
//////// C++ std::map handling
//////%include "std_map.i"
//////
//////// C++ std::map handling
//////%include "std_set.i"
//////
//////// C++ std::map handling
//////%include "std_vector.i"
//////
//////%include "stl.i"
//////
////////enables better handling of STL exceptions
//////%include "exception.i"

%exception {
  try {
    $action
  } catch (const std::exception& e) {
    SWIG_exception(SWIG_RuntimeError, e.what());
  }
}

// %include "swig_includes/numpy.i"
// // // %include "pyinterface/swig_includes/numpy.i"

// // // %init %{
    // // // import_array();
// // // %}


//C arrays
//%include "carrays.i"

// ******************************
// Third Party Classes
// ******************************
#define CAPDESOLVERS_EXPORT

//%include <CompuCell3D/Field3D/Point3D.h>
//%include <CompuCell3D/Field3D/Dim3D.h>


%include <CompuCell3D/Field3D/Array3D.h>

//%template(Array3DContiguousFloat) CompuCell3D::Array3DContiguous<float>;

//////
//////%include <CA/modules/PDESolvers/DiffusableVectorCommon.h>
//////

//////%template(stdvectorstring) std::vector<std::string>;

//%ignore CompuCell3D::SecretionData::secretionConst;
%include <CA/modules/CAPDESolvers/DiffSecrData.h>
%include <CA/modules/CAPDESolvers/DiffusionSolverFE.h>

%extend CompuCell3D::DiffusionSolverFE{
      %pythoncode %{
    def addFieldsPy(self,_fieldList):
        print '_fieldList=',_fieldList
        self.addFields(['FGF','VEGF'])            
	

    def addField(self,*args,**kwds):
        
        try:
            fieldName=kwds['Name']
            self.addDiffusionAndSecretionData(fieldName)
            diffData = self.getDiffusionData(fieldName)
            secrData = self.getSecretionData(fieldName)
        except LookupError:
            raise AttributeError('The field you define needs to have a name! Use "Name" as an argument of the "addField" function')
        
        diffDataPy=None
        secrDataPy=None
        try:
            diffDataPy=kwds['DiffusionData']
        except LookupError:
            pass 
                
        try:
            secrDataPy=kwds['SecretionData']
        except LookupError:
            pass 

        try:
            diffData.diffConst = diffDataPy['DiffusionConstant']
        except LookupError:
            pass 

        try:
            diffData.decayConst = diffDataPy['DecayConstant']
        except LookupError:
            pass 

        
        for typeName in secrDataPy.keys():
            
            secrData.setTypeNameSecrConst(typeName,secrDataPy[typeName])

	%}


};

