#ifndef VIENNACL_TOOLS_MATRIX_SIZE_DEDUCER_HPP_
#define VIENNACL_TOOLS_MATRIX_SIZE_DEDUCER_HPP_

/* =========================================================================
   Copyright (c) 2010-2012, Institute for Microelectronics,
                            Institute for Analysis and Scientific Computing,
                            TU Wien.
   Portions of this software are copyright by UChicago Argonne, LLC.

                            -----------------
                  ViennaCL - The Vienna Computing Library
                            -----------------

   Project Head:    Karl Rupp                   rupp@iue.tuwien.ac.at
               
   (A list of authors and contributors can be found in the PDF manual)

   License:         MIT (X11), see file LICENSE in the base directory
============================================================================= */

/** @file viennacl/tools/matrix_size_deducer.hpp
    @brief Helper implementations that deduce the dimensions of the supplied matrix-valued expressions.
*/

#include <string>
#include <fstream>
#include <sstream>
#include "viennacl/forwards.h"
#include "viennacl/tools/adapter.hpp"

#include <vector>
#include <map>

namespace viennacl
{
  namespace tools
  {

    /** @brief Deduces the size of the resulting vector represented by a vector_expression from the operands
    *
    * @tparam LHS   The left hand side operand
    * @tparam RHS   The right hand side operand
    * @tparam OP    The operation tag
    */
    template <typename LHS, typename RHS, typename OP>
    struct MATRIX_SIZE_DEDUCER
    {
      //Standard case: size1 from lhs, size2 from rhs (fits most cases)
      static std::size_t size1(LHS & lhs, RHS & /*rhs*/) { return lhs.size1(); }
      static std::size_t size2(LHS & /*lhs*/, RHS & rhs) { return rhs.size2(); }
    };

    
    //special case: outer vector product:
    template <typename ScalarType, unsigned int A1, unsigned int A2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::vector<ScalarType, A1>,
                               const viennacl::vector<ScalarType, A2>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::vector<ScalarType, A1> const & lhs,
                               viennacl::vector<ScalarType, A2> const & /*rhs*/) { return lhs.size(); }

      static std::size_t size2(viennacl::vector<ScalarType, A1> const & /*lhs*/,
                               viennacl::vector<ScalarType, A2> const & rhs) { return rhs.size(); }
    };

    //special case: multiplication with a GPU scalar
    template <typename ScalarType, typename F, unsigned int A>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix<ScalarType, F, A>,
                               const viennacl::scalar<ScalarType>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix<ScalarType, F, A> const & lhs,
                               viennacl::scalar<ScalarType> const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix<ScalarType, F, A> const & lhs,
                               viennacl::scalar<ScalarType> const & /*rhs*/) { return lhs.size2(); }
    };
    
    //special case: multiplication with a CPU scalar
    template <typename ScalarType, typename F, unsigned int A>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix<ScalarType, F, A>,
                               const ScalarType,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix<ScalarType, F, A> const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix<ScalarType, F, A> const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size2(); }
    };
    
    
    //special case: multiplication with a GPU scalar for a matrix_range
    template <typename MatrixType, typename T>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_range<MatrixType>,
                               const viennacl::scalar<T>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_range<MatrixType> const & lhs,
                               viennacl::scalar<T> const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix_range<MatrixType> const & lhs,
                               viennacl::scalar<T> const & /*rhs*/) { return lhs.size2(); }
    };
    
    //special case: multiplication with a CPU scalar for a matrix_range
    template <typename ScalarType, typename F, unsigned int A>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_range<viennacl::matrix<ScalarType, F, A> >,
                               const ScalarType,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_range<viennacl::matrix<ScalarType, F, A> > const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix_range<viennacl::matrix<ScalarType, F, A> > const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size2(); }
    };
    
    

    //special case: multiplication with a GPU scalar for a matrix_slice
    template <typename MatrixType, typename T>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_slice<MatrixType>,
                               const viennacl::scalar<T>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_slice<MatrixType> const & lhs,
                               viennacl::scalar<T> const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix_slice<MatrixType> const & lhs,
                               viennacl::scalar<T> const & /*rhs*/) { return lhs.size2(); }
    };
    
    //special case: multiplication with a CPU scalar for a matrix_slice
    template <typename ScalarType, typename F, unsigned int A>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_slice<viennacl::matrix<ScalarType, F, A> >,
                               const ScalarType,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_slice<viennacl::matrix<ScalarType, F, A> > const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size1(); }

      static std::size_t size2(viennacl::matrix_slice<viennacl::matrix<ScalarType, F, A> > const & lhs,
                               ScalarType const & /*rhs*/) { return lhs.size2(); }
    };
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    //special case: transposed matrix-vector product: Return the number of rows of the matrix
    template <typename MatrixType>
    struct MATRIX_SIZE_DEDUCER<MatrixType,
                               MatrixType,
                               viennacl::op_trans>
    {
      static std::size_t size1(const MatrixType & lhs,
                               const MatrixType & /*rhs*/) { return lhs.size2(); }
      static std::size_t size2(const MatrixType & lhs,
                               const MatrixType & /*rhs*/) { return lhs.size1(); }
    };

    // A^T * B
    template <typename ScalarType, typename T1, typename F2, unsigned int A2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_expression<T1,
                                                                 T1, op_trans>,
                               const viennacl::matrix<ScalarType, F2, A2>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & lhs,
                               viennacl::matrix<ScalarType, F2, A2> const & /*rhs*/) { return lhs.lhs().size2(); }
      static std::size_t size2(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & /*lhs*/,
                               viennacl::matrix<ScalarType, F2, A2> const & rhs) { return rhs.size2(); }
    };

    template <typename T1, typename MatrixType2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_expression<T1,
                                                                 T1, op_trans>,
                               const viennacl::matrix_range<MatrixType2>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & lhs,
                               viennacl::matrix_range<MatrixType2> const & /*rhs*/) { return lhs.lhs().size2(); }
      static std::size_t size2(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & /*lhs*/,
                               viennacl::matrix_range<MatrixType2> const & rhs) { return rhs.size2(); }
    };

    template <typename T1, typename MatrixType2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_expression<T1,
                                                                 T1, op_trans>,
                               const viennacl::matrix_slice<MatrixType2>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & lhs,
                               viennacl::matrix_slice<MatrixType2> const & /*rhs*/) { return lhs.lhs().size2(); }
      static std::size_t size2(viennacl::matrix_expression<T1,
                                                           T1,
                                                           op_trans> const & /*lhs*/,
                               viennacl::matrix_slice<MatrixType2> const & rhs) { return rhs.size2(); }
    };
    
    
    // A * B^T 
    
    template <typename ScalarType, typename F1, unsigned int A1, typename T2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix<ScalarType, F1, A1>,
                               const viennacl::matrix_expression<T2,
                                                                 T2, op_trans>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix<ScalarType, F1, A1> const & lhs,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & /*rhs*/) { return lhs.size1(); }
      static std::size_t size2(viennacl::matrix<ScalarType, F1, A1> const & /*lhs*/,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & rhs) { return rhs.lhs().size1(); }
    };

    template <typename MatrixType1, typename T2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_range<MatrixType1>,
                               const viennacl::matrix_expression<T2,
                                                                 T2, op_trans>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_range<MatrixType1> const & lhs,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & /*rhs*/) { return lhs.size1(); }
      static std::size_t size2(viennacl::matrix_range<MatrixType1> const & /*lhs*/,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & rhs) { return rhs.lhs().size1(); }
    };

    template <typename MatrixType1, typename T2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_slice<MatrixType1>,
                               const viennacl::matrix_expression<T2,
                                                                 T2, op_trans>,
                               viennacl::op_prod>
    {
      static std::size_t size1(viennacl::matrix_slice<MatrixType1> const & lhs,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & /*rhs*/) { return lhs.size1(); }
      static std::size_t size2(viennacl::matrix_slice<MatrixType1> const & /*lhs*/,
                               viennacl::matrix_expression<T2,
                                                           T2,
                                                           op_trans> const & rhs) { return rhs.lhs().size1(); }
    };

    
    
    // A^T * B^T 
    
    template <typename T1, typename T2>
    struct MATRIX_SIZE_DEDUCER<const viennacl::matrix_expression<T1,
                                                                 T1, op_trans>,
                               const viennacl::matrix_expression<T2,
                                                                 T2, op_trans>,
                               viennacl::op_prod>
    {
      typedef viennacl::matrix_expression<T1, T1, op_trans>   LHSType;
      typedef viennacl::matrix_expression<T2, T2, op_trans>   RHSType;
      
      static std::size_t size1(LHSType const & lhs,
                               RHSType const & /*rhs*/) { return lhs.lhs().size2(); }
      static std::size_t size2(LHSType const & /*lhs*/,
                               RHSType const & rhs) { return rhs.lhs().size1(); }
    };
    
  }
}

#endif

