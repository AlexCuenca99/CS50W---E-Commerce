from django.db.models import fields
from django.forms import widgets
from django import forms

from .models import *


class AuctionListForm(forms.ModelForm):
    class Meta:
        model = AuctionList
        fields = ["title", "description", "startingBid", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "autofocus": "",
                    "class": "block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-100 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Insert a title",
                    "id": "title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-100 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Insert a description",
                    "id": "description",
                }
            ),
            "startingBid": forms.NumberInput(
                attrs={
                    "class": "block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-100 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Insert a starting bid",
                    "id": "startingBid",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "block w-full px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-100 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Insert a starting bid",
                    "id": "category",
                }
            ),
        }


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ["picture", "optText"]
        widgets = {
            "picture": forms.FileInput(
                attrs={
                    "class": "w-11/12 transition duration-500 ease-in-out transform border rounded-md text-md focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                }
            ),
            "optText": forms.TextInput(
                attrs={
                    "class": "w-11/12 mt-3 px-5 py-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-100 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Insert a description",
                    "id": "optText",
                    "value": "None",
                }
            ),
        }


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["offer"]
        widgets = {
            "offer": forms.NumberInput(
                attrs={
                    "autofocus": "",
                    "class": "px-5 py-3 ml-3 mr-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-500",
                    "placeholder": "Take my bid",
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "autofocus": "",
                    "placeholder": "Type a title for your comment",
                    "class": "block w-full px-5 py-3 m-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-300",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Type your comment",
                    "class": "block w-full px-5 py-3 m-3 text-base text-neutral-600 placeholder-gray-300 transition duration-500 ease-in-out transform border border-transparent rounded-lg bg-gray-50 focus:outline-none focus:border-transparent focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-yellow-300",
                }
            ),
        }
