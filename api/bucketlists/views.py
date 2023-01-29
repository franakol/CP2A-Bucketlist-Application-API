from flask_restx import Namespace,Resource,fields
from ..models.bucketlists import Bucketlist
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..models.users import User
from ..models.items import Item
from ..utils import db
from werkzeug.exceptions import Conflict, BadRequest
from flask import request
from datetime import datetime


bucketlist_namespace=Namespace('bucketlists',description="a namespace for bucketlists")



bucketlist_model=bucketlist_namespace.model(
    'Bucketlist',{
        'bucket_id':fields.Integer(description="An id"),
        'name':fields.String(description="Name of the bucket list"),
        'date_created':fields.DateTime(description="date of creation of the bucket list"),
        'date_modified':fields.DateTime(description="date of modification of the bucket list"),
        'created_by':fields.Integer(description="user that created the bucket list")
    
    }

)

item_model=bucketlist_namespace.model(
    'Item',{
        'item_id':fields.Integer(description="An id"),
        'name':fields.String(description="Name of the bucketlist item"),
        'date_created':fields.DateTime(description="date of creation of the bucketlist item"),
        'date_modified':fields.DateTime(description="date of modification of the bucketlist item"),
        'bucket_id':fields.Integer(description="bucket id"),

        
    
    }

)
@bucketlist_namespace.route('/')
class BucketlistGetCreate(Resource):

    @bucketlist_namespace.expect(bucketlist_model)
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Create a new bucket list"
    )
    @jwt_required()
    def post(self):
        """
           Create a new bucket list
        """

        username=get_jwt_identity()

        current_user=User.query.filter_by(username=username).first()
        

        data=bucketlist_namespace.payload
    
        new_bucketlist=Bucketlist(
            name=data['name'],
            date_created=data['date_created'],
            created_by=current_user.user_id,
            
        )

        new_bucketlist.created_by=current_user.user_id

        new_bucketlist.save()

        return new_bucketlist , HTTPStatus.CREATED
         
   

    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="List all the created bucket lists"
    )
    @jwt_required()
    def get(self):

        """
           List all the created bucket lists
        """
        bucketlists=Bucketlist.query.all()

        return bucketlists ,HTTPStatus.OK

@bucketlist_namespace.route('/<int:bucket_id>')
class GetUpdateDelete(Resource):


    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Get single bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
    @jwt_required()
    def get(self,bucket_id):
        """
           Get single bucket list
        """
        bucketlist=Bucketlist.query.get(bucket_id)
        

        return bucketlist ,HTTPStatus.OK

    @bucketlist_namespace.expect(bucketlist_model)
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="Update this bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist",
            "name": "Name of a  given bucketlist",

        }
    )
    @jwt_required()
    def put(self,bucket_id):
        """
           Update this bucket list
        """
        

        bucketlist_to_update=Bucketlist.query.get(bucket_id)

        data=bucketlist_namespace.payload

        bucketlist_to_update.name=data['name']
        bucketlist_to_update.date_created=data['date_created']
        bucketlist_to_update.date_modified=data['date_modified']
        bucketlist_to_update.created_by=data['created_by'].user_id

        db.session.commit()

        return bucketlist_to_update, HTTPStatus.OK


    @jwt_required()
    @bucketlist_namespace.marshal_with(bucketlist_model)
    @bucketlist_namespace.doc(
        description="delete this single bucket list",
        params={
            "bucketlist_id":"An ID for a given bucketlist"

        }
    )
    def delete(self,bucket_id):
        """
           Delete this single bucket list
        """
        bucketlist_to_delete=Bucketlist.query.get(bucket_id)

        bucketlist_to_delete.delete()

        return bucketlist_to_delete, HTTPStatus.OK


@bucketlist_namespace.route('/<int:bucket_id>/items')
class Get(Resource):

   
   @bucketlist_namespace.marshal_with(item_model)
   @bucketlist_namespace.expect(item_model)
   @jwt_required()
   def post(self, bucket_id):
        """
            Create a new item in bucket list        
        """
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        data = request.json
        new_item = Item(
            name=data['name'],
            date_created=datetime.now(),
            bucket_id=bucket_id
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item, HTTPStatus.CREATED



@bucketlist_namespace.route('/<int:bucket_id>/items/<int:item_id>')

class UpdateDelete(Resource):

    @bucketlist_namespace.doc(
        description="Update a bucket list item",
        params={
            "bucketlist_id":"An ID for a given bucketlist",
            "item_id":"An item ID"

        }
    )

    def put(self,bucket_id,item_id):
        """
            Update a bucket list item
        """
        data=bucketlist_namespace.payload
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.name = data['name']
            item.date_created = data['date_created']
            item.save()
            return item, HTTPStatus.OK
        else:
            return {"error": "item not found"}, HTTPStatus.NOT_FOUND
    
    @bucketlist_namespace.doc(
        description="Delete an item in a bucket list",
         params={
            "bucketlist_id":"An ID for a given bucketlist",
            "item_id":"An item ID"

        }
    )

    def delete(self,bucket_id,item_id):
        """
            Delete an item in a bucket list
        """
        
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.delete()
            return {"message": "item deleted successfully"}, HTTPStatus.OK
        else:
            return {"error": "item not found"}, HTTPStatus.NOT_FOUND

