/**
 * @file    XMLTriple.cpp
 * @brief   Stores an XML namespace triple.
 * @author  Ben Bornstein
 * 
 * <!--------------------------------------------------------------------------
 * This file is part of libSBML.  Please visit http://sbml.org for more
 * information about SBML, and the latest version of libSBML.
 *
 * Copyright (C) 2009-2012 jointly by the following organizations: 
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. EMBL European Bioinformatics Institute (EBML-EBI), Hinxton, UK
 *  
 * Copyright (C) 2006-2008 by the California Institute of Technology,
 *     Pasadena, CA, USA 
 *  
 * Copyright (C) 2002-2005 jointly by the following organizations: 
 *     1. California Institute of Technology, Pasadena, CA, USA
 *     2. Japan Science and Technology Agency, Japan
 * 
 * This library is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation.  A copy of the license agreement is provided
 * in the file named "LICENSE.txt" included with this software distribution and
 * also available online as http://sbml.org/software/libsbml/license.html
 * ---------------------------------------------------------------------- -->*/

#include <sbml/xml/XMLTriple.h>
#include <sbml/util/util.h>
#include <sbml/xml/XMLAttributes.h>
#include <sbml/xml/XMLConstructorException.h>

/** @cond doxygen-ignored */

using namespace std;

/** @endcond */

LIBSBML_CPP_NAMESPACE_BEGIN

/*
 * Creates a new empty XMLTriple.
 */
XMLTriple::XMLTriple ()
{
}


/*
 * Creates a new XMLTriple.
 */
XMLTriple::XMLTriple (  const std::string&  name
                      , const std::string&  uri
                      , const std::string&  prefix ) 
{
  if ((&name == NULL) || (&uri == NULL) || (&prefix == NULL))
    throw XMLConstructorException("Null argument given to constructor");

  mName = name;
  mURI = uri;
  mPrefix = prefix;
}


/*
 * Creates a new XMLTriple by splitting triplet on sepchar.  Triplet
 * may be in one of the following formats:
 *
 *   name
 *   uri sepchar name
 *   uri sepchar name sepchar prefix
 */
XMLTriple::XMLTriple (const std::string& triplet, const char sepchar)
{ 
  if (&triplet == NULL)
    throw XMLConstructorException("NULL reference in XML constructor");

  string::size_type start = 0;
  string::size_type pos   = triplet.find(sepchar, start);


  if (pos != string::npos)
  {
    mURI = triplet.substr(start, pos);

    start = pos + 1;
    pos   = triplet.find(sepchar, start);

    if (pos != string::npos)
    {
      mName   = triplet.substr(start, pos - start);
      mPrefix = triplet.substr(pos + 1);
    }
    else
    {
      mName = triplet.substr(start);
    }
  }
  else
  {
    mName = triplet;
  }
}


/*
 * Copy constructor; creates a copy of this XMLTriple set.
 */
XMLTriple::XMLTriple(const XMLTriple& orig)
{
  if (&orig == NULL)
  {
    throw XMLConstructorException("Null argument to copy constructor");
  }
  else
  {
    mName   = orig.mName;
    mURI    = orig.mURI;
    mPrefix = orig.mPrefix;
  }
}


/*
 * Assignment operator for XMLTriple.
 */
XMLTriple& 
XMLTriple::operator=(const XMLTriple& rhs)
{
  if (&rhs == NULL)
  {
    throw XMLConstructorException("Null argument to assignment operator");
  }
  else if(&rhs!=this)
  {
    mName   = rhs.mName;
    mURI    = rhs.mURI;
    mPrefix = rhs.mPrefix;
  }

  return *this;
}


/*
 * Creates and returns a deep copy of this XMLTriple set.
 * 
 * @return a (deep) copy of this XMLTriple set.
 */
XMLTriple* 
XMLTriple::clone () const
{
  return new XMLTriple(*this);
}


/*
 * @return a string, the name from this XMLTriple.
 */
const std::string&
XMLTriple::getName () const
{
  return mName;
}


/*
 * @return a string, the @em prefix portion of this XMLTriple.
 */
const std::string& 
XMLTriple::getPrefix () const
{
  return mPrefix;
}


/*
 * @return URI a string, the @em prefix portion of this XMLTriple.
 */
const std::string&
XMLTriple::getURI () const
{
  return mURI;
}


/*
 * @return prefixed name from this XMLTriple.
 */
const std::string 
XMLTriple::getPrefixedName () const
{
  return mPrefix + ((mPrefix != "") ? ":" : "") + mName;
}


/*
 * @return true if this XMLTriple set is empty, false otherwise.
 */
bool
XMLTriple::isEmpty () const
{
  return ( getName().size() == 0
        && getURI().size() == 0
        && getPrefix().size() == 0);
}


/*
 * Comparison (equal-to) operator for XMLTriple.
 *
 * @return @c non-zero (true) if the combination of name, URI, and 
 * prefix of lhs is equal to that of rhs @c zero (false) otherwise.
 */
bool operator==(const XMLTriple& lhs, const XMLTriple& rhs)
{
  if (lhs.getName()   != rhs.getName()  ) return false;
  if (lhs.getURI()    != rhs.getURI()   ) return false;
  if (lhs.getPrefix() != rhs.getPrefix()) return false;

  return true;
}


/*
 * Comparison (not equal-to) operator for XMLTriple.
 *
 * @return @c non-zero (true) if the combination of name, URI, and 
 * prefix of lhs is not equal to that of rhs @c zero (false) otherwise.
 */
bool operator!=(const XMLTriple& lhs, const XMLTriple& rhs)
{
  return !(lhs == rhs);
}

/** @cond doxygen-c-only */


/**
 * Creates a new empty XMLTriple_t structure and returns a pointer to it.
 *
 * @return pointer to created XMLTriple_t structure.
 */
LIBLAX_EXTERN
XMLTriple_t *
XMLTriple_create (void)
{
  return new(nothrow) XMLTriple;
}


/**
 * Creates a new XMLTriple_t structure with name, prefix and uri.
 *
 * @param name a string, name for the XMLTriple_t structure.
 * @param uri a string, URI of the XMLTriple_t structure.
 * @param prefix a string, prefix for the URI of the XMLTriple_t structure.
 *
 * @return pointer to the created XMLTriple_t structure.
   */
LIBLAX_EXTERN
XMLTriple_t *
XMLTriple_createWith (const char *name, const char *uri, const char *prefix)
{
  if (name == NULL || uri == NULL || prefix == NULL) return NULL;
  return new(nothrow) XMLTriple(name, uri, prefix);
}


/**
 * Destroys this XMLTriple_t structure.
 *
 * @param triple XMLTriple_t structure to be freed.
 **/
LIBLAX_EXTERN
void
XMLTriple_free (XMLTriple_t *triple)
{
  if (triple == NULL) return; 
  delete static_cast<XMLTriple*>( triple );
}


/**
 * Creates a deep copy of the given XMLTriple_t structure
 * 
 * @param t the XMLTriple_t structure to be copied
 * 
 * @return a (deep) copy of the given XMLTriple_t structure.
 */
LIBLAX_EXTERN
XMLTriple_t *
XMLTriple_clone (const XMLTriple_t* t)
{
  if (t == NULL) return NULL;
  return static_cast<XMLTriple*>( t->clone() );
}


/**
 * Returns the name from this XMLTriple_t structure.
 *
 * @param triple XMLTriple_t structure to be queried.
 *
 * @return name from this XMLTriple_t structure.
 */
LIBLAX_EXTERN
const char *
XMLTriple_getName (const XMLTriple_t *triple)
{
  if (triple == NULL) return NULL;
  return triple->getName().empty() ? NULL : triple->getName().c_str();
}


/**
 * Returns the prefix from this XMLTriple_t structure.
 *
 * @param triple XMLTriple_t structure to be queried.
 *
 * @return prefix from this XMLTriple_t structure.
 */
LIBLAX_EXTERN
const char *
XMLTriple_getPrefix (const XMLTriple_t *triple)
{
  if (triple == NULL) return NULL;
  return triple->getPrefix().empty() ? NULL : triple->getPrefix().c_str();
}


/**
 * Returns the URI from this XMLTriple_t structure.
 *
 * @param triple XMLTriple_t structure to be queried.
 *
 * @return URI from this XMLTriple_t structure.
 */
LIBLAX_EXTERN
const char *
XMLTriple_getURI (const XMLTriple_t *triple)
{
  if (triple == NULL) return NULL;
  return triple->getURI().empty() ? NULL : triple->getURI().c_str();
}


/**
 * Returns the prefixed name from this XMLTriple_t structure.
 *
 * @param triple XMLTriple_t structure to be queried.
 *
 * @return prefixed name from this XMLTriple_t structure.
 */
LIBLAX_EXTERN
const char *
XMLTriple_getPrefixedName (const XMLTriple_t *triple)
{
  if (triple == NULL) return NULL;
  return triple->getPrefixedName().empty() ? NULL : safe_strdup(triple->getPrefixedName().c_str());
}


/**
 * Predicate returning @c true or @c false depending on whether 
 * this XMLTriple is empty.
 * 
 * @param triple XMLTriple_t structure to be queried.
 *
 * @return @c non-zero (true) if this XMLTriple is empty, @c zero (false) otherwise.
 */
LIBLAX_EXTERN
int
XMLTriple_isEmpty (const XMLTriple_t *triple)
{
  if (triple == NULL) return (int)true;
  return static_cast<int> (triple->isEmpty());
}


/**
 * Predicate returning @c true or @c false depending on whether 
 * this XMLTriple is equal to the given XMLTriple.
 * 
 * @param lhs XMLTriple_t structure to be required.
 * @param rhs XMLTriple_t structure to be compared with this XMLTriple.
 *
 * @return @c non-zero (true) if the combination of name, URI, and prefix of this
 * XMLTriple is equal to that of the given XMLTriple, 
 * @c zero (false) otherwise.
 */
LIBLAX_EXTERN
int
XMLTriple_equalTo(const XMLTriple_t *lhs, const XMLTriple_t* rhs)
{
  if (lhs == NULL && rhs == NULL) return (int) true;
  if (lhs == NULL || rhs == NULL) return (int) false;
  return (*lhs == *rhs);
}


/**
 * Predicate returning @c true or @c false depending on whether 
 * this XMLTriple is not equal to the given XMLTriple.
 * 
 * @param lhs XMLTriple_t structure to be required.
 * @param rhs XMLTriple_t structure to be compared with this XMLTriple.
 *
 * @return @c non-zero (true) if the combination of name, URI, and prefix of this
 * XMLTriple is not equal to that of the given XMLTriple, 
 * @c zero (false) otherwise.
 */
LIBLAX_EXTERN
int
XMLTriple_notEqualTo(const XMLTriple_t *lhs, const XMLTriple_t* rhs)
{
  return (int) !((bool)XMLTriple_equalTo(lhs, rhs));
}



/** @endcond */

LIBSBML_CPP_NAMESPACE_END
