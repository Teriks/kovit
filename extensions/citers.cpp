// Copyright (c) 2018, Teriks
// All rights reserved.
//
// kovit is distributed under the following BSD 3-Clause License
//
// Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
// ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


#include "Python.h"

#include <vector>
#include <list>


typedef struct {
    PyObject_HEAD
    PyObject *sequence;
    std::list<PyObject*> *stack;
    size_t span_size;
} Iter_Runs_State;


typedef struct {
    PyObject_HEAD
    PyObject *sequence;
    std::list<PyObject*> *stack;
    size_t window_size;
} Iter_Window_State;



static PyObject *
iter_runs_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyObject *sequence;
    PyObject *span_size;

    if (!PyArg_UnpackTuple(args, "iter_runs", 1, 2, &sequence, &span_size))
        return NULL;

    if(PySequence_Check(sequence)) {
        sequence = PySeqIter_New(sequence);
    }
    else if (!PyIter_Check(sequence)) {
        PyErr_SetString(PyExc_TypeError, "iter_runs() expects an iterable");
        return NULL;
    }

    Iter_Runs_State *istate = (Iter_Runs_State *)type->tp_alloc(type, 0);

    if (!istate)
        return NULL;

    Py_INCREF(sequence);


    istate->sequence = sequence;
    istate->span_size = PyLong_AsLong(span_size);
    istate->stack = new std::list<PyObject*>();

    return (PyObject *)istate;
}


static PyObject *
iter_window_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    PyObject *sequence;
    PyObject *window_size;

    if (!PyArg_UnpackTuple(args, "iter_window", 1, 2, &sequence, &window_size))
        return NULL;

    if(PySequence_Check(sequence)) {
        sequence = PySeqIter_New(sequence);
    }
    else if (!PyIter_Check(sequence)) {
        PyErr_SetString(PyExc_TypeError, "iter_window() expects an iterable");
        return NULL;
    }

    Iter_Window_State *istate = (Iter_Window_State *)type->tp_alloc(type, 0);

    if (!istate)
        return NULL;

    Py_INCREF(sequence);

    istate->sequence = sequence;
    istate->window_size = PyLong_AsLong(window_size) + 1;
    istate->stack = new std::list<PyObject*>();

    return (PyObject *)istate;
}


static void
iter_runs_dealloc(Iter_Runs_State *istate)
{
    delete istate->stack;
    Py_XDECREF(istate->sequence);
    Py_TYPE(istate)->tp_free(istate);
}


static void
iter_window_dealloc(Iter_Window_State *istate)
{
    delete istate->stack;
    Py_XDECREF(istate->sequence);
    Py_TYPE(istate)->tp_free(istate);
}


static PyObject *
iter_runs_next(Iter_Runs_State *istate)
{
    std::list<PyObject*> *stack = istate->stack;

    PyObject *item = PyIter_Next(istate->sequence);

    PyObject* first = stack->size() > 0 ? stack->back() : 0;

    stack->clear();

    if(item) {
        if(!first) {
            first = item;
        } else {
            stack->push_back(item);
        }
    }

    while(stack->size() < istate->span_size && (item = PyIter_Next(istate->sequence))) {
        stack->push_back(item);
    }

    if(stack->size() > 0) {
        PyObject* tup = PyTuple_New(stack->size());

        std::list<PyObject*>::const_iterator iter(stack->begin());

        for(size_t idx = 0; iter != stack->end(); iter++, idx++) {
            PyObject* i = *iter;
            PyTuple_SET_ITEM(tup, idx, i);
            Py_INCREF(i);
        }

        PyObject* r = PyTuple_Pack(2, first, tup);
        Py_DECREF(tup);
        return r;
    }

    if(first){
        PyObject* tup = PyTuple_New(0);
        PyObject* r = PyTuple_Pack(2, first, tup);
        Py_DECREF(tup);
        return r;
    }

    return NULL;
}


static PyObject *
iter_window_next(Iter_Window_State *istate)
{
    PyObject* item;

    size_t idx = istate->stack->size();
    size_t lim = istate->window_size;

    while(idx < lim && (item = PyIter_Next(istate->sequence))) {
        istate->stack->push_back(item);
        idx++;
    }

    if(idx == 0) {
        return NULL;
    }

    PyObject* first = istate->stack->front();
    istate->stack->pop_front();

    PyObject* tup = PyTuple_New(idx - 1);

    std::list<PyObject*>::const_iterator iter(istate->stack->begin());

    for(idx=0; iter != istate->stack->end(); iter++, idx++) {
        PyObject* i = *iter;
        PyTuple_SET_ITEM(tup, idx, i);
        Py_INCREF(i);
    }

    PyObject* r = PyTuple_Pack(2, first, tup);
    Py_DECREF(tup);
    return r;
}


PyTypeObject PyIter_Runs_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "iter_runs",                    /* tp_name */
    sizeof(Iter_Runs_State),        /* tp_basicsize */
    0,                              /* tp_itemsize */
    (destructor)iter_runs_dealloc,  /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    0,                              /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    PyObject_SelfIter,              /* tp_iter */
    (iternextfunc)iter_runs_next,   /* tp_iternext */
    0,                              /* tp_methods */
    0,                              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    PyType_GenericAlloc,            /* tp_alloc */
    iter_runs_new,                  /* tp_new */
};


PyTypeObject PyIter_Window_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "iter_window",                /* tp_name */
    sizeof(Iter_Window_State),    /* tp_basicsize */
    0,                            /* tp_itemsize */
    (destructor)iter_window_dealloc,     /* tp_dealloc */
    0,                              /* tp_print */
    0,                              /* tp_getattr */
    0,                              /* tp_setattr */
    0,                              /* tp_reserved */
    0,                              /* tp_repr */
    0,                              /* tp_as_number */
    0,                              /* tp_as_sequence */
    0,                              /* tp_as_mapping */
    0,                              /* tp_hash */
    0,                              /* tp_call */
    0,                              /* tp_str */
    0,                              /* tp_getattro */
    0,                              /* tp_setattro */
    0,                              /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,             /* tp_flags */
    0,                              /* tp_doc */
    0,                              /* tp_traverse */
    0,                              /* tp_clear */
    0,                              /* tp_richcompare */
    0,                              /* tp_weaklistoffset */
    PyObject_SelfIter,              /* tp_iter */
    (iternextfunc)iter_window_next, /* tp_iternext */
    0,                              /* tp_methods */
    0,                              /* tp_members */
    0,                              /* tp_getset */
    0,                              /* tp_base */
    0,                              /* tp_dict */
    0,                              /* tp_descr_get */
    0,                              /* tp_descr_set */
    0,                              /* tp_dictoffset */
    0,                              /* tp_init */
    PyType_GenericAlloc,            /* tp_alloc */
    iter_window_new,              /* tp_new */
};


static struct PyModuleDef kovi_iters_module = {
    PyModuleDef_HEAD_INIT,
    "citers",          /* m_name */
    "",                /* m_doc */
    -1,                /* m_size */
};


PyMODINIT_FUNC
PyInit_citers(void)
{
    PyObject *module = PyModule_Create(&kovi_iters_module);

    if (!module)
        return NULL;

    if (PyType_Ready(&PyIter_Runs_Type) < 0)
        return NULL;

    if (PyType_Ready(&PyIter_Window_Type) < 0)
        return NULL;


    Py_INCREF(&PyIter_Runs_Type);
    if(PyModule_AddObject(module, "iter_runs", (PyObject *)&PyIter_Runs_Type) < 0){
        return NULL;
    }

    Py_INCREF(&PyIter_Window_Type);
    if(PyModule_AddObject(module, "iter_window", (PyObject *)&PyIter_Window_Type) < 0){
        return NULL;
    }

    return module;
}